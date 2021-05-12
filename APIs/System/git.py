from __future__ import annotations

import gitlab
from gitlab.v4.objects import ProjectCommit

GITLAB_TOKEN = 'zjZcRyys41iRSPkF1JDr'


class BotItGitIssue:
    def __init__(self, title: str, description: str, labels: [str], is_closed: bool = False):
        self.title: str = title
        self.description: str = description
        self.labels: [str] = labels
        self.labels.append('From Bot')
        self.is_closed: bool = is_closed


class BotItGitCommit:
    def __init__(self, message: str, author: str, time_changed: str):
        self.message = message
        self.author = author
        self.time_changed = time_changed


class BotItGit:
    """

    A class for interacting with the TalpiBot git(lab) repository.
    Can be used for sending new issues, etc.

    """

    __instance = None

    def __init__(self):
        if BotItGit.__instance is not None:
            raise Exception("This class is a singleton!")

        BotItGit.__instance = self

        self.gitlab_project = None
        self.connect_to_gitlab()

    @staticmethod
    def get() -> BotItGit:
        if BotItGit.__instance is None:
            BotItGit()
        return BotItGit.__instance

    def connect_to_gitlab(self):
        gitlab_connection = gitlab.Gitlab('https://gitlab.com/', private_token=GITLAB_TOKEN)

        # search for TalpiBot project
        projects = gitlab_connection.projects.list(owned=True)
        self.gitlab_project = None
        for _project in projects:
            if _project.name == "TalpiBot":
                self.gitlab_project = _project
                break
        if self.gitlab_project is None:
            raise Exception("TalpiBot Project was not found with this API token.")

    def create_new_issue(self, issue_object: BotItGitIssue):
        issue = self.gitlab_project.issues.create({'title': issue_object.title,
                                                   'description': issue_object.description})
        issue.labels = issue_object.labels
        if issue_object.is_closed:
            issue.state_event = 'close'
        issue.save()

    def get_last_commit(self) -> BotItGitCommit:
        last_raw_commit: ProjectCommit = self.gitlab_project.commits.list()[0]
        return BotItGitCommit(message=last_raw_commit.attributes['message'],
                              author=last_raw_commit.attributes['author_name'],
                              time_changed=last_raw_commit.attributes['committed_date'])


if __name__ == '__main__':
    BotItGit.get().get_last_commit()
