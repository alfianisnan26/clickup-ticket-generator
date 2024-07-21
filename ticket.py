from logger import logger

import requests

import constants
from checklist import Checklist
from thread_manager import ThreadPoolLimiter


class Ticket:
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

    def create(self, thread_manager: ThreadPoolLimiter):
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

        thread_manager.submit(self.__do_create_task, request=request, thread_manager=thread_manager)

    def __do_create_task(self, request, thread_manager: ThreadPoolLimiter):
        response = requests.post(constants.URL_TASK_CREATE.format(list_id=constants.LIST_ID),
                                 json=request,
                                 headers={"Authorization": constants.API_KEY})

        if response.status_code != 200:
            exception = Exception("Failed to create task", response.status_code, response.text)
            logger.error(exception)
            raise exception

        self.id = response.json()["id"]

        if self.checklists:
            thread_manager.submit(self.__do_create_checklist, thread_manager=thread_manager)

        parent_id = None
        if self.parent:
            parent_id = self.parent.id

        logger.info(f"Success push: {self.id} of {parent_id} | {self.title}")

        thread_manager.submit(self.__do_create_subtask, thread_manager=thread_manager)

    def __do_create_checklist(self, thread_manager: ThreadPoolLimiter):
        request = {
            "name": self.checklist_name
        }

        response = requests.post(constants.URL_CHECKLIST_CREATE.format(task_id=self.id),
                                 json=request,
                                 headers={"Authorization": constants.API_KEY})

        if response.status_code != 200:
            exception = Exception("Failed to create checklist", response.status_code, response.text)
            logger.error(exception)
            raise exception

        checklist_id = response.json()["checklist"]["id"]

        for checklist in self.checklists:
            thread_manager.submit(Checklist(*checklist).with_id(checklist_id).create)

    def __do_create_subtask(self, thread_manager: ThreadPoolLimiter):
        for child in self.children:
            if self.synced_child:
                child.create(thread_manager=thread_manager)
            else:
                thread_manager.submit(child.create, thread_manager=thread_manager)
