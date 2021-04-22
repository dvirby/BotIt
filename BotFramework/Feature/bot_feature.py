from abc import ABC, abstractmethod
from typing import Type
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.ui.ui import UI
from APIs.ExternalAPIs.Scheduler.scheduler import ScheduledJob
from BotFramework.bot_user import BotUser


class BotFeature(ABC):

    @abstractmethod
    def __init__(self, ui: UI):
        self.ui = ui

        for job in self.get_scheduled_jobs():
            job.schedule()

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []

    @abstractmethod
    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        pass

    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        return []

    @abstractmethod
    def is_authorized(self, user: Type[BotUser]) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        pass
