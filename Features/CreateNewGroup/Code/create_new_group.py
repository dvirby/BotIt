from BotFramework import *
from APIs.ExternalAPIs import *
from APIs.OtherAPIs.DatabaseRelated import User
from BotFramework.Activity import FormActivity
from APIs.OtherAPIs.DatabaseRelated.Group.create_group_form import CreateGroupForm
from APIs.OtherAPIs.DatabaseRelated.Group import groups

class CreateNewGroup(BotFeature):

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        self.ui.create_form_view(session, CreateGroupForm(), "please insert the following details:",
                         self.func1).draw()

    def func1(self, session: Session, form_activity: FormActivity, form: CreateGroupForm):
        groups.create_new_group(str(form.groupName.value), str(form.description.value), form.participants.value, [session.user])
        self.ui.create_text_view(session, "Group successfully created!").draw()


    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        pass

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "bot_admin" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []
