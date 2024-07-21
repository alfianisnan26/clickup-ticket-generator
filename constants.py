import os

LIST_ID = os.getenv("LIST_ID")
REVIEWER_ID = os.getenv("REVIEWER_ID")
API_KEY = os.getenv("API_KEY")

URL_TASK_CREATE = "https://api.clickup.com/api/v2/list/{list_id}/task"
URL_CHECKLIST_CREATE = "https://api.clickup.com/api/v2/task/{task_id}/checklist"
URL_CHECKLIST_CREATE_ITEM = "https://api.clickup.com/api/v2/checklist/{checklist_id}/checklist_item"