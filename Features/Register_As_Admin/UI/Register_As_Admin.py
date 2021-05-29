from OtherAPIs.Constraint.UserConstraint.user_constraint import MachzorConstraint

from APIs.ExternalAPIs import *
from APIs.OtherAPIs.Constraint.UserConstraint.user_constraint import UserConstraint
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.ui.ui import UI
from APIs.OtherAPIs.DatabaseRelated.User.user import User
from BotFramework.Activity.FormActivity.form_activity import FormActivity
from BotFramework.admin_register_form import AdminRegisterForm

class Register_As_Admin(BotFeature):

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
        buttons = []
        buttons.append(self.ui.create_button_view("Log in", self.func1))
        buttons.append(self.ui.create_button_view("Sing up", self.func2))

        self.ui.create_button_group_view(session, "What do you want to do?", buttons).draw()

    def func1(self, session: Session):
        form = AdminRegisterForm()
        self.ui.create_form_view(session, form, "Log in as admin", self.func3).draw()

    def func2(self, session: Session):
        form = AdminRegisterForm()
        self.ui.create_form_view(session, form, "Sing up as admin", self.func4).draw()

    def func3(self, session: Session, form_activity: FormActivity, form: AdminRegisterForm):
        users = UserConstraint.get_users_with_constraint(MachzorConstraint(User().mahzor))
        t = 0
        for user in users:
            if user.adminUsername == form.username.value and user.adminPassword == form.password.value:
                self.ui.create_text_view(session, "You are registered as: " + user.name).draw()
                t = 1
        if t == 0:
            self.ui.create_text_view(session,"Invalid username or password").draw()
            form = AdminRegisterForm()
            self.ui.create_form_view(session, form, "Log in as admin", self.func3).draw()
        else:
            user = session.user
            user.adminPassword = form.password.value
            user.adminUsername = form.username.value
            user.role.append("admin")
            user.save()

    def func4(self, session: Session, form_activity: FormActivity, form: AdminRegisterForm):
        users = UserConstraint.get_users_with_constraint(MachzorConstraint(User().mahzor))
        t = 0
        for user in users:
            if user.adminUsername == form.username.value and user.adminPassword == form.password.value:
                self.ui.create_text_view(session, "This username and password is already taken").draw()
                t = 1
        if t == 1:
            newForm = AdminRegisterForm()
            self.ui.create_form_view(session, newForm, "Sing up as admin", self.func4()).draw()
        else:
            user = session.user
            user.adminPassword = form.password.value
            user.adminUsername = form.username.value
            user.role.append("admin")
            user.save()
            self.ui.create_text_view(session, "You are registered as: " + str(user.name)).draw()







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
