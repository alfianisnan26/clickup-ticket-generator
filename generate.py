import asyncio
import csv
import os
from typing import Callable, List

import requests
from slugify import slugify


class AsyncJobRunner:
    gathered_async_task = []

    def __init__(self, max_jobs: int = 5):
        self.max_jobs = max_jobs
        self.semaphore = asyncio.Semaphore(max_jobs)

    async def _run_job(self, coro: Callable, *args, **kwargs):
        async with self.semaphore:
            return await coro(*args, **kwargs)

    async def run_jobs(self, jobs: List[Callable], *args, **kwargs):
        tasks = [self._run_job(job, *args, **kwargs) for job in jobs]
        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    def run_task(coro: Callable, *args, **kwargs):
        loop = asyncio.get_event_loop()
        task = loop.create_task(coro(*args, **kwargs))
        AsyncJobRunner.gathered_async_task.append(task)

    @staticmethod
    async def wait():
        await asyncio.gather(*AsyncJobRunner.gathered_async_task)


class Checklist:
    async def create(self):
        request = {
            "name": self.name,
            "assignee": self.assignee
        }

        response = requests.post(Ticket.URL_CHECKLIST_CREATE_ITEM.format(checklist_id=self.checklist_id),
                                 json=request,
                                 headers={"Authorization": Ticket.API_KEY})
        if response.status_code != 200:
            exception = Exception("Failed to create checklist item", response.status_code, response.text)
            print(exception)
            raise exception

        print(f"Success push: checklist [{self.name}] of {self.checklist_id}")

    def __init__(self, name=None, assignee=None):
        self.checklist_id = None
        self.name = name
        self.assignee = assignee

    def with_id(self, checklist_id):
        self.checklist_id = checklist_id
        return self


class Ticket:
    LIST_ID = os.getenv("LIST_ID")
    REVIEWER_ID = os.getenv("REVIEWER_ID")
    API_KEY = os.getenv("API_KEY")

    URL_TASK_CREATE = "https://api.clickup.com/api/v2/list/{list_id}/task"
    URL_CHECKLIST_CREATE = "https://api.clickup.com/api/v2/task/{task_id}/checklist"
    URL_CHECKLIST_CREATE_ITEM = "https://api.clickup.com/api/v2/checklist/{checklist_id}/checklist_item"

    def __init__(self, template=None, checklists=None, checklist_name="Approval"):
        self.synced_child = None
        self.parent = None
        self.effort = None
        self.tags = None
        self.description = None
        self.title = None

        self.template = template
        self.checklists = checklists
        self.checklist_name = checklist_name
        self.children = []

    def prepare(self, title="Sample Task", description=None, tags=None, effort=None, parent=None, synced_child=False):
        self.title = title
        self.description = description
        self.tags = tags
        self.effort = effort
        self.parent = parent

        self.synced_child = synced_child

        if self.parent:
            self.parent.children.append(self)

    async def create(self):
        request = {
            "name": self.title,
            "markdown_description": self.description or self.title,
            "tags": self.tags,
            "status": "Open",
            "notify_all": False,
        }

        if self.parent:
            request["parent"] = self.parent.id

        if self.template:
            with open("./templates/" + self.template, "r") as f:
                template = f.read()
                request["markdown_description"] = template.format(description=self.description)

        if self.effort:
            effort = str(self.effort).strip()
            effort = effort.replace(",", ".")
            request["time_estimate"] = int(float(effort) * 6 * 60 * 60 * 1000)

        id = self.__do_create_task(request)

        parent_id = None
        if self.parent:
            parent_id = self.parent.id

        print(f"Success push: {id} of {parent_id} | {self.title}")

        AsyncJobRunner.run_task(self.__do_create_subtask)

    def __do_create_task(self, request):
        response = requests.post(Ticket.URL_TASK_CREATE.format(list_id=Ticket.LIST_ID),
                                 json=request,
                                 headers={"Authorization": Ticket.API_KEY})

        if response.status_code != 200:
            exception = Exception("Failed to create task", response.status_code, response.text)
            print(exception)
            raise exception

        self.id = response.json()["id"]

        if self.checklists:
            AsyncJobRunner.run_task(self.__do_create_checklist)

        return self.id  # task_id for parenthesis

    async def __do_create_checklist(self):
        request = {
            "name": self.checklist_name
        }

        response = requests.post(Ticket.URL_CHECKLIST_CREATE.format(task_id=self.id),
                                 json=request,
                                 headers={"Authorization": Ticket.API_KEY})

        if response.status_code != 200:
            exception = Exception("Failed to create checklist", response.status_code, response.text)
            print(exception)
            raise exception

        checklist_id = response.json()["checklist"]["id"]

        job_runner = AsyncJobRunner()
        jobs = [Checklist(*checklist).with_id(checklist_id).create for checklist in self.checklists]
        await job_runner.run_jobs(jobs)

    async def __do_create_subtask(self):
        job_runner = AsyncJobRunner()
        if self.synced_child:
            for child in self.children:
                await child.create()
        else:
            await job_runner.run_jobs([child.create for child in self.children])


CHECKLIST_MENTOR = ("Mentor", None)
CHECKLIST_REVIEWER = ("Reviewer", os.getenv("REVIEWER_ID"))

TICKET_PROJECT_TEMPLATE = ("project_task.md", [CHECKLIST_MENTOR, CHECKLIST_REVIEWER])
TICKET_MATERI_TEMPLATE = ("materi_task.md", [CHECKLIST_MENTOR, CHECKLIST_REVIEWER])
TICKET_LEVEL_TEMPLATE = ("level_task.md", [CHECKLIST_MENTOR, CHECKLIST_REVIEWER])
TICKET_MENTORING_TEMPLATE = ("mentoring_task.md", [CHECKLIST_REVIEWER])
TICKET_COACHING_TEMPLATE = ("coaching_task.md", [CHECKLIST_REVIEWER])

LEVEL_TITLE_TEMPLATE = "[LEVEL | {grade}-L{kd}] Level Tracker"


def build_description(description=None, links=None, month=None, semester=None):
    result = ""
    if description:
        result = description + "\n"

    if month or semester:
        result += f"### Target pembelajaran:\n"
        if month:
            result += f"- Bulan ke: **{month}**\n"
        if semester:
            result += f"- Semester ke: **{semester}**\n"

    if links:
        result += f"### Referensi belajar:\n"
        for link in links:
            result += f"- {link}\n"

    return result


class GeneratorHandler:
    def __init__(self, total_rows):
        self.total_rows = total_rows
        self.level_cursor = 0
        self.current_line = 0
        self.level_ticket = None
        self.materi_ticket = None

    def progress(self):
        progress = self.current_line / self.total_rows * 100
        self.current_line += 1

        return progress

    def check_level(self, level):
        if self.level_cursor != level:
            self.level_cursor = level
            return True

        return False


async def generator(f):
    reader = csv.DictReader(f)

    total_rows = 0

    raw_document = []
    for row in reader:
        total_rows += 1
        raw_document.append(row)

    handler = GeneratorHandler(total_rows)

    document = []

    for row in raw_document:
        level = row["Level"]
        kategori = row["Kategori"]
        nama_tiket = row["Nama Tiket"]
        grade = row["Grade"]
        materi = row["Materi"]
        kd = row["KD"]
        effort = row["Effort"]
        description = row["Kata Kunci"]
        link = row["Link Belajar"]
        month = row["Monts"]
        semester = row["Semester (5 mos)"]

        progress = handler.progress()

        if handler.check_level(level):
            if kategori != "Project":
                handler.level_ticket = Ticket(*TICKET_LEVEL_TEMPLATE)
                handler.level_ticket.prepare(
                    LEVEL_TITLE_TEMPLATE.format(grade=grade[:2], kd=kd),
                    tags=["level", slugify(grade)],
                    synced_child=True
                )

                document.append(handler.level_ticket)

                print(f"[ {progress:6.2f} % ]", "Created level ticket\t" + nama_tiket)

        if kategori == "Project":
            project_ticket = Ticket(*TICKET_PROJECT_TEMPLATE)
            project_ticket.prepare(
                nama_tiket,
                description=build_description(
                    description=description,
                    links=[link],
                    month=month,
                    semester=semester,
                ),
                tags=["materi", slugify(kategori), slugify(materi), slugify(grade)],
                effort=effort
            )

            document.append(project_ticket)

            print(f"[ {progress:6.2f} % ]", "Created project ticket\t" + nama_tiket)
        else:
            materi_ticket = Ticket(*TICKET_MATERI_TEMPLATE)
            materi_ticket.prepare(
                nama_tiket,
                description=build_description(
                    description=description,
                    links=[link],
                    month=month,
                    semester=semester,
                ),
                tags=["materi", slugify(kategori), slugify(materi), slugify(grade)],
                effort=effort,
                parent=handler.level_ticket)

            Ticket(*TICKET_COACHING_TEMPLATE).prepare(
                title="[COACHING] #Nomor Urut",
                tags=["coaching"],
                parent=materi_ticket,
            )

            Ticket(*TICKET_MENTORING_TEMPLATE).prepare(
                title="[MENTORING] Nama Mentee",
                tags=["mentoring"],
                parent=materi_ticket,
            )

            print(f"[ {progress:6.2f} % ]", "Created materi ticket\t" + nama_tiket)

    for doc in document:
        await doc.create()


async def main():
    with open(os.getenv("CSV_FILE"), "r") as f:
        await generator(f)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    AsyncJobRunner.wait()

    loop.close()
