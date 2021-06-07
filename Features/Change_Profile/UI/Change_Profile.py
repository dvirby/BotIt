from APIs.ExternalAPIs import *
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.ui.ui import UI
from APIs.OtherAPIs.DatabaseRelated.User.user import User
from APIs.OtherAPIs.DatabaseRelated.User.user_detailes_form import UserDetailesForm
from BotFramework.Activity.FormActivity.form_activity import FormActivity

hisID = ""
hisPwd = ""
hisSchool = ""
class Change_Profile(BotFeature):

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
        self.ui.create_form_view(session, UserDetailesForm(), "please insert the following details:",
                                 self.func1).draw()
    def func1(self, session: Session, form_activity: FormActivity, form: UserDetailesForm):
        user = session.user
        user.email = str(form.eMail.value)
        user.name = str(form.name.value)
        user.save()
        if form.is_admin.value == ['yes']:
            self.ui.create_text_view(session, "What is the admin password?").draw()
            self.ui.get_text(session, self.passwordCorrect)
        else:
            self.ui.create_text_view(session, "You are registered!").draw()

    def passwordCorrect(self, session, text):
        if str(text) == '123456789':
            user = session.user
            user.role.append('bot_admin')
            user.save()
            self.ui.create_text_view(session, "You are registered as admin!").draw()
        else:
            self.ui.create_text_view(session, "Wrong password!").draw()


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
        return "מתלם" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []
