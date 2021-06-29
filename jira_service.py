import requests
from requests.auth import HTTPBasicAuth
import pdb
import json
import os
from datetime import datetime


class JiraService:

    def __init__(self):
        email = os.environ['JIRA_EMAIL']
        key = os.environ['JIRA_API_KEY']
        self.auth = HTTPBasicAuth(email, key) 
        self.jira_cache = {}

    def try_post_time(self, data):
        for item in data:
            if not item['jira']:
                item['status'] = 'NA'
                continue
            if self.was_already_submitted(item):
                item['status'] = "Already posted"
                continue
            url = f"https://lendio.atlassian.net/rest/api/3/issue/{item['issue']}/worklog"
            payload = {'started': item['started'].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'-0600'}
            payload['timeSpentSeconds'] = item['timeSpentSeconds']
            response = requests.post(url, auth=self.auth, json=payload)
            if (response.status_code >= 200 and response.status_code < 300):
                item['status'] = "Posted"
            else:
                item['status'] = "Not posted: " + response.text
        return data

    def was_already_submitted(self, item):
        issue = item['issue']
        entries = self.jira_cache[issue] if issue in self.jira_cache else self.get_worklog_for_issue(issue)
        return item['started'].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'-0600' in entries

    def get_worklog_for_issue(self, issue):
        url = f"https://lendio.atlassian.net/rest/api/3/issue/{issue}/worklog"
        response = requests.get(url, auth=self.auth)
        worklog = json.loads(response.text)
        entries = [a['started'] for a in worklog['worklogs']] 
        self.jira_cache[issue] = entries
        return entries

