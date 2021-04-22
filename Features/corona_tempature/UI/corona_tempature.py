import pickle
import threading

from BotFramework import *
from BotFramework.Activity.FormActivity.form_activity import FormActivity
from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.ui.ui import UI, Button
from APIs.TalpiotAPIs.User.user import User

from Features.corona_tempature.Logic.data_view import CoronaForm


class CoronaTemperature(BotFeature):
    """
        This first version will only work with Mahzor 41, blame Iyar Mazor
        Author Barr Kirel, 41
    """
    # Survey links for temperature control, mahzor: link
    GROUPS_LINKS = {41: ["אייר מזור"]}
    SURVEY_MESSAGE = "סקר הקורונה😷 \n\nשימו לב במידה ואין תסימינים נא לא למלא כלום.\n לחץ על השדות בכדי למלא"
    # This is a dictionary used to keep who filled the survey and who didn't
    unfilled = {}
    # Just to keep amounts in a lazy way
    total_amount = {}

    FILE_NAME = "unfilled_corona.pkl"
    file_lock = threading.Lock()

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)
        self.load_pickle()

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        mahzor = session.user.mahzor
        name = session.user.name
        if mahzor not in self.GROUPS_LINKS:
            self.ui.create_text_view(session, "לא נתמך").draw()
            return
        if name not in self.GROUPS_LINKS[mahzor]:
            self.show_survey(session)
            return
        # Fill Survey
        # View unfilled
        # Remind to fill
        buttons = [self.ui.create_button_view("😷 מלא סקר", self.show_survey),
                   self.ui.create_button_view("👀 צפה במי לא מילא", self.view_unfilled),
                   self.ui.create_button_view("✉ תזכר את כולם למלא", self.send_all),
                   self.ui.create_button_view("❌ אל תעשה כלום", lambda x: self.ui.clear(x))]
        self.ui.create_button_group_view(session, "מה תרצה לעשות?", buttons).draw()

    def view_unfilled(self, session):
        mahzor = session.user.mahzor
        if mahzor not in self.GROUPS_LINKS:
            self.ui.create_text_view(session, "לא נתמך").draw()
            return
        unfilled = self.get_unfilled(mahzor)
        unfilled.sort()
        users = "המשתמשים שעוד לא מילאו את הסקר" + " (%d/%d) :" % (len(unfilled), self.total_amount[mahzor])
        for user in unfilled:
            users += f"\n[❌] %s" % user
        self.ui.create_text_view(session, users).draw()
        buttons = [self.ui.create_button_view("כן", lambda x: self.ui.clear(x))]
        self.ui.create_button_group_view(session, "למחוק את ההודעה", buttons).draw()

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
        return user.mahzor in self.GROUPS_LINKS

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        regular = ScheduledJob(self.remind_admins, [], day_of_week="0,1,2,3,4,6", hour="8,9,10,11", minute="30")
        shabat = ScheduledJob(self.remind_admins, [], day_of_week="5", hour="21,22", minute="00,30")
        reset_users = ScheduledJob(self.reset_users, [], day_of_week="*", hour="1", minute="00")
        return [regular, shabat, reset_users]

    def send_options(self, session):
        self.ui.create_text_view(session, "Don't forget to fill the corona survey").draw()

    def reset_users(self):
        """
        This function will re-add all the users to the unfilled list
        """
        for group in self.GROUPS_LINKS:
            if group in self.unfilled:
                del self.unfilled[group]
            self.unfilled[group] = [user.name for user in
                                    UserConstraint.get_users_with_constraint(MachzorConstraint(group))]
            self.total_amount[group] = len(self.unfilled[group])
        self.update_pickle()
        for admin in self.get_admins():
            admin_ses = self.ui.create_session("corona_temp", admin)
            self.ui.create_text_view(admin_ses, "[[Corona Bot 😷]]\n %s מחקתי את רשימת ממלאי הסקר" % admin).draw()

    # This is a function just to make the code more readable
    def get_unfilled(self, group):
        return self.unfilled[group]

    def display_options(self, user):
        user = UserConstraint.get_users_with_constraint(
            NameUserConstraint(user))[0]
        session = self.ui.create_session("corona_tempature", user)
        mahzor = user.mahzor
        if mahzor not in self.GROUPS_LINKS:
            return
        buttons = [self.ui.create_button_view("😷 אני אמלא עכשיו", self.show_survey),
                   self.ui.create_button_view("❌ לא, תזכיר לי אחר כך", self.keep_in_list)]
        message = "מילאת סקר קורונה?😷"
        self.ui.create_button_group_view(session, message, buttons).draw()

    def remove_from_unfilled(self, session):
        mahzor = session.user.mahzor
        if mahzor not in self.GROUPS_LINKS:
            return
        self.unfilled[mahzor].remove(session.user)
        self.ui.clear(session)
        self.ui.create_text_view(session, "אחלה תודה!").draw()
        if len(self.unfilled[mahzor]) == 0:
            for admin in self.get_admins():
                if admin.mahzor == mahzor:
                    sess = self.ui.create_session("corona_temp", admin)
                    self.ui.create_text_view(sess, "[[Corona Bot 😷]]\n %s כל המחזור מילא את הסקר" % admin).draw()

    def keep_in_list(self, session):
        self.ui.clear(session)
        self.ui.create_text_view(session, "אחלה אזכיר לך אחר כך").draw()

    def send_all(self, garbage):
        """
        This function sends all the users that didn't fill the survey a reminder to fill it
        """
        for group in self.unfilled:
            for user in self.unfilled[group]:
                self.display_options(user)

    def remind_admins(self):
        """
        This function sends all the users that didn't fill the survey a reminder to fill it
        """
        for admin in self.get_admins():
            temp_sess = self.ui.create_session("קורונה", admin)
            mahzor = admin.mahzor
            users = "משתמשים שעוד לא מילאו את הסקר" + " (%d/%d)" % (
                len(self.unfilled[mahzor]), self.total_amount[mahzor])
            self.ui.create_text_view(temp_sess, users).draw()

    def get_admins(self):
        """
        This function returns the alfi corona
        """
        admins = []
        for mahzor in self.GROUPS_LINKS:
            for admin in self.GROUPS_LINKS[mahzor]:
                admins += UserConstraint.get_users_with_constraint(NameUserConstraint(admin))
        return admins

    def show_survey(self, session, ignore=False):
        mahzor = session.user.mahzor
        name = session.user.name
        if mahzor not in self.GROUPS_LINKS:
            self.ui.create_text_view(session, "לא נתמך עליידי המחזור שלך").draw()
        if not ignore and name not in self.unfilled[mahzor]:
            buttons = [self.ui.create_button_view("כן", lambda x: self.show_survey(x, True)),
                       self.ui.create_button_view("לא", lambda x: self.ui.clear(session))]
            self.ui.create_button_group_view(session, "כבר מילאת את הסקר, תרצה למלא שוב?", buttons).draw()
            return
        form = CoronaForm()
        self.ui.create_form_view(session, form, self.SURVEY_MESSAGE, self.fill_survey).draw()

    def fill_survey(self, session, form_activity: FormActivity, obj: CoronaForm):
        mahzor = session.user.mahzor
        name = session.user.name
        temperature = obj.temperature.value
        symptoms = obj.symptoms.value
        family = obj.family.value
        try:
            temperature = float(temperature)
        except ValueError as e:
            self.ui.create_text_view(session, "נא להכניס מספר בתור הטמפרטורה!").draw()
            return
        except TypeError as e:
            self.ui.create_text_view(session, "נא למלא את שדה הטמפרטורה !").draw()
            return
        if symptoms == "אין":
            symptoms = None
        # Now we test if there is a problem in the survey
        invalid = temperature < 36 or temperature > 37 or symptoms is not None or family
        if invalid:
            # Send a message to the person incharge
            message = "%s had a problem with his survey\nTemperature: %.2f\nSymptoms: %s\nFamily in isolation: %s"
            if mahzor not in self.GROUPS_LINKS:
                self.ui.create_text_view(session, "לא הצלחנו למצוא את האחראי קורונה שלך, שלח לו את ההודעה הבאה").draw()
                self.ui.create_text_view(session, message % (name, temperature, symptoms, family)).draw()
            else:
                for admin in self.GROUPS_LINKS[mahzor]:
                    temp_sess = self.ui.create_session("קורונה", UserConstraint.get_users_with_constraint(
                        NameUserConstraint(admin))[0])
                    self.ui.create_text_view(temp_sess, message % (name, temperature, symptoms, family)).draw()
        form_activity.remove()
        if mahzor not in self.GROUPS_LINKS:
            return
        if session.user.name in self.unfilled[mahzor]:
            self.unfilled[mahzor].remove(session.user.name)
            self.update_pickle()
        self.ui.clear(session)
        self.ui.create_text_view(session, "תודה שמילאת את הסקר").draw()
        if len(self.unfilled[mahzor]) == 0:
            for admin in self.GROUPS_LINKS[mahzor]:
                sess = self.ui.create_session("corona_temp", admin)
                self.ui.create_text_view(sess, "[[Corona Bot 😷]]\n %s כל המחזור מילא את הסקר" % admin).draw()

    def update_pickle(self):
        try:
            self.file_lock.acquire()
            with open(self.FILE_NAME, 'wb') as output:  # Overwrites any existing file.
                pickle.dump(self.unfilled, output, pickle.HIGHEST_PROTOCOL)
        except:
            self.file_lock.release()

    def load_pickle(self):
        try:
            with open(self.FILE_NAME, "rb") as input:
                self.unfilled = pickle.load(input)
            for group in self.GROUPS_LINKS:
                self.total_amount[group] = len(UserConstraint.get_users_with_constraint(MachzorConstraint(group)))
        except:
            self.reset_users()
