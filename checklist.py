import requests

import constants
from logger import logger


class Checklist:
    def create(self):
        request = {
            "name": self.name,
            "assignee": self.assignee
        }

        response = requests.post(constants.URL_CHECKLIST_CREATE_ITEM.format(checklist_id=self.checklist_id),
                                 json=request,
                                 headers={"Authorization": constants.API_KEY})
        if response.status_code != 200:
            exception = Exception("Failed to create checklist item", response.status_code, response.text)
            logger.error(exception)
            raise exception

        logger.info(f"Success push: checklist [{self.name}] of {self.checklist_id}")

    def __init__(self, name=None, assignee=None):
        self.checklist_id = None
        self.name = name
        self.assignee = assignee

    def with_id(self, checklist_id):
        self.checklist_id = checklist_id
        return self

