import csv
import os

from slugify import slugify

from generator_handler import GeneratorHandler
from thread_manager import ThreadPoolLimiter
from ticket import Ticket

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


def generator(f):


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

        if handler.check_level(level):
            if kategori != "Project":
                handler.level_ticket = Ticket(*TICKET_LEVEL_TEMPLATE)
                handler.level_ticket.prepare(
                    LEVEL_TITLE_TEMPLATE.format(grade=grade[:2], kd=kd),
                    tags=["level", slugify(grade)],
                    synced_child=True
                )

                document.append(handler.level_ticket)
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

    thread_manager = ThreadPoolLimiter(num_threads=5, rate=1.65)

    for doc in document[:]:
        doc.create(thread_manager=thread_manager)

    thread_manager.wait_until_finish()


if __name__ == "__main__":
    with open(os.getenv("CSV_FILE"), "r") as f:
        generator(f)
