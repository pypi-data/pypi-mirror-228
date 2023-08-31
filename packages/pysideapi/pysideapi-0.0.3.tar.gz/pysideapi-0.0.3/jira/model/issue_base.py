from datetime import datetime
from typing import List

import pytz

from jira.model.issue_status import IssueStatus

tz = pytz.timezone('America/Lima')


class IssueBase:
    def __init__(self):
        self.id = ''
        self.key = ''
        self.title = ''
        self.issue_type_id = ''
        self.issue_type_name = ''
        self.description = ''
        self.assignee_name = ''
        self.assignee_email = ''
        self.creator_name = ''
        self.creator_email = ''
        self.status_id = ''
        self.status_name = ''
        self.create_date = ''
        self.update_date = ''
        self.historical_status_change = []
        self.labels = ''

    def _convert_histories_to_status(self, json_histories):

        for story in json_histories:
            items = story.get('items')
            for item in items:
                if item.get('field') == 'status':
                    issue_status = IssueStatus()
                    finish = datetime.strptime(story.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
                    finish = finish.astimezone(tz)
                    finish = finish.strftime("%Y-%m-%d %H:%M:%S")
                    issue_status.from_status_id = item.get('from')
                    issue_status.from_status_name = item.get('fromString')
                    issue_status.to_status_id = item.get('to')
                    issue_status.to_status_name = item.get('toString')
                    issue_status.status_change_date = finish
                    issue_status.modifier_name = story.get("author").get("displayName")
                    issue_status.modifier_email = story.get("author").get("emailAddress")
                    issue_status.issue_key = self.key
                    self.historical_status_change.append(issue_status)


