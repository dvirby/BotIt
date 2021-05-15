from BotFramework.Activity.FormActivity.form_activity import FormActivity
from APIs.ExternalAPIs import *
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.ui.ui import UI
from APIs.OtherAPIs.DatabaseRelated.User.user import User
from Features.Classrooms.Logic.class_logic import *
from Features.Classrooms.Logic.order_classroom_form import OrderClassroomForm
from Features.Classrooms.Logic.reset_dbs import *


ADMIN = "inbar.gil.41@gmail.com"


class Classrooms(BotFeature):

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
        buttons = [
            self.ui.create_button_view("🏕️ הזמנת כיתה", self.order_classroom),
            self.ui.create_button_view("🏕️ כיתות שהזמנתי", self.view_classrooms),
            self.ui.create_button_view("🏕️ כל ההזמנות", self.admin_classrooms),
            self.ui.create_button_view("🏕️ פעולות שגמ\"ח", self.admin_actions),
            self.ui.create_button_view("🔙", lambda s: self.return_to_menu(s))]
        self.ui.create_button_group_view(session, "הזמנת כיתות", buttons).draw()

    def admin_actions(self, session: Session):
        self.ui.clear(session)
        if session.user.email == ADMIN:
            buttons = [
                self.ui.create_button_view("ריסט כיתות", lambda s: self.reset_classroom_db(s)),
                self.ui.create_button_view("ריסט אירועים קודמים", lambda s: self.reset_event_db(s, date=datetime.now().date())),
                self.ui.create_button_view("יצירת אירוע מפקדה", self.choose_date_hq)
            ]
            self.ui.create_button_group_view(session, "אדמין", buttons).draw()
        else:
            self.ui.summarize_and_close(session, views=[self.ui.create_text_view(session, "אין לך גישה לפעולה זו")])

    def reset_event_db(self, session: Session, date: date):
        reset_event_db(date)
        self.ui.summarize_and_close(session, views=[self.ui.create_text_view(session, "המאגר רוסט")])

    def reset_classroom_db(self, session: Session):
        reset_classroom_db()
        self.ui.summarize_and_close(session, views=[self.ui.create_text_view(session, "המאגר רוסט")])

    def choose_date_hq(self, session: Session):
        self.ui.clear(session)
        self.ui.create_date_choose_view(session, lambda v, s, d: self.create_hq_event(s, d)).draw()

    def create_hq_event(self, session: Session, date: date):
        class_buttons = []
        classroom_list = Classroom.objects()
        self.ui.clear(session)
        date_text = date.strftime(' %a\' - %d/%m/%y')
        start_time = f"/{8} {00}"
        start_time = datetime.strptime(date_text + start_time,
                                        " %a\' - %d/%m/%y/%H %M")
        end_time = f"/{17} {00}"
        end_time = datetime.strptime(date_text + end_time,
                                       " %a\' - %d/%m/%y/%H %M")
        for classroom in classroom_list:
                class_buttons.append(
                    self.ui.create_button_view(f"{classroom.name}",
                                               lambda s,
                                                      c=classroom: self.event_creation(
                                                   s, date,
                                                   [start_time, end_time],
                                                   session.user, c)))
        self.ui.create_button_group_view(session, "כיתות אפשריות", class_buttons).draw()

    def return_to_menu(self, session: Session):
        from Features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import \
            HierarchicalMenu
        self.ui.clear(session)
        HierarchicalMenu.run_menu(self.ui, session.user)

    def admin_classrooms(self, session: Session):
        self.ui.clear(session)
        if session.user.email == ADMIN:
            self.ui.create_date_choose_view(session,
                                            lambda v, s,
                                                   d: self.display_hq_events(s,
                                                                             d)).draw()
        else:
            self.ui.summarize_and_close(session, views=[
                self.ui.create_text_view(session,
                                         "אינך בעל הרשאות לשימוש בפיצ'ר זה בבוט")])

    def return_to_main(self, session: Session):
        self.ui.clear(session)
        self.ui.clear(session)
        self.main(session)

    def display_hq_events(self, session: Session, date: date):
        self.ui.clear(session)
        events = ClassroomEvent.objects(date=date)
        events = sorted(events, key=lambda x: x.start_time)
        buttons_list = []
        date_text = date.strftime(' %a\' - %d/%m/%y')
        time_text = f"/{23} {59}"
        hq_end_time = datetime.strptime(date_text + time_text,
                                        " %a\' - %d/%m/%y/%H %M")
        for event in events:
            if event.start_time < hq_end_time:
                buttons_list.append(
                    self.ui.create_button_view(event.get_title(), lambda s,
                                                                         e=event: self.display_hq_event(
                                                                         s, e)))

        if buttons_list:
            buttons_list.append(self.ui.create_button_view("🔙", self.return_to_main))
            self.ui.create_button_group_view(session,
                                             "אירועים שמתנגשים עם המפקדה",
                                             buttons_list).draw()
        else:
            self.ui.summarize_and_close(session,
                                        views=[self.ui.create_text_view(session,
                                                                        "אין אירועים מתנגשים")])

    def display_hq_event(self, session: Session, event: ClassroomEvent):
        self.ui.clear(session)
        text = event.get_full_details()
        buttons_list = [self.ui.create_button_view("מחק", lambda
            s: self.delete_hq_event(s, event)),
                        self.ui.create_button_view("🔙", lambda
            s: self.display_hq_events(s, event.date))]
        self.ui.create_button_group_view(session,
                                         f"למחוק את האירוע הבא?\n{text}",
                                         buttons_list).draw()

    def delete_hq_event(self, session: Session, event: ClassroomEvent):
        event.delete_self()
        self.ui.clear(session)
        text = event.get_full_details() + "אירוע זה לא אושר כי הוא מתנגש עם לו\"ז אחר.\nתנסו לקבוע אותו בכיתה או זמן אחר."
        finish_view = self.ui.create_text_view(session, "הזמנת הכיתה נמחקה")
        self.ui.summarize_and_close(session, views=[finish_view])
        user_session = self.ui.create_session("Classrooms", event.user)
        self.ui.create_text_view(user_session, text).draw()

    def order_classroom(self, session: Session):
        self.ui.clear(session)
        cur_date = datetime.now()

        fv = self.ui.create_form_view(session, OrderClassroomForm(), "בחר פרטים להזמנה", self.choose_classroom)
        fv.draw()

    def choose_classroom(self, session: Session, form_activity: FormActivity, form: OrderClassroomForm):
        #  Validate Form
        form.validate()

        #  Check
        date = form.date.value
        start_time = datetime.combine(date, form.start_time.value.time())
        end_time = datetime.combine(date, form.end_time.value.time())

        class_buttons = []
        classroom_list = Classroom.objects()
        self.ui.clear(session)
        for classroom in classroom_list:
            if get_free_classes(date, [start_time, end_time], classroom):
                class_buttons.append(
                    self.ui.create_button_view(f"{classroom.name}",
                                               lambda s,
                                                      c=classroom: self.create_event(
                                                   s, date,
                                                   [start_time, end_time],
                                                   session.user, c)))
        if class_buttons:
            class_buttons.append(self.ui.create_button_view("🔙", self.return_to_main))
            self.ui.create_button_group_view(session, "כיתות זמינות בזמן שבחרת:",
                                             class_buttons).draw()
        else:
            self.ui.summarize_and_close(session, views=[self.ui.create_text_view(session, "אין כיתות זמינות בזמן שבחרת.")])

    def create_event(self, session: Session, date: date, hours: list, user: User, classroom: Classroom):
        date_text = date.strftime(' %a\' - %d/%m/%y')
        time_text = f"/{17} {00}"
        hq_end_time = datetime.strptime(date_text + time_text,
                                        " %a\' - %d/%m/%y/%H %M")
        if hours[0] < hq_end_time:
            buttons_list = [
                self.ui.create_button_view("כן", lambda s: self.event_creation(s, date, hours, user, classroom)),
                self.ui.create_button_view("לא", lambda s: self.ask_to_review(s))
            ]
            self.ui.create_button_group_view(session, "האם ביררתם עם השגמ\"ח כיתות שהכיתה הזו אכן זמינה בשעה שבחרתם?", buttons_list).draw()
        else:
            self.event_creation(session, date, hours, user, classroom)

    def ask_to_review(self, session: Session):
        self.ui.clear(session)
        finish_view = self.ui.create_text_view(session, "תוודאו עם השגמ\"ח כיתות שהסלוט הזה אכן פנוי")
        self.ui.summarize_and_close(session, views=[finish_view])

    def event_creation(self, session: Session, date: date, hours: list, user: User, classroom: Classroom):
        create_event(date, hours, user, classroom)
        self.ui.clear(session)
        finish_view = self.ui.create_text_view(session, "הכיתה הוזמנה")
        self.ui.summarize_and_close(session, views=[finish_view])

    def view_classrooms(self, session: Session):
        self.ui.clear(session)
        classroom_list = ClassroomEvent.objects(user=session.user)
        button_list = []
        for event in classroom_list:
            if event.start_time < datetime.now():
                continue

            button_list.append(self.ui.create_button_view(event.get_title(),
                                                          lambda s,
                                                                 e=event: self.display_event(
                                                              s, e)))
        if button_list:
            button_list.append(self.ui.create_button_view("🔙", self.return_to_main))
            self.ui.create_button_group_view(session, "אירועים שלך:",
                                             button_list).draw()
        else:
            finish_view = self.ui.create_text_view(session, "לא שריינת כיתות")
            self.ui.summarize_and_close(session, views=[finish_view])

    def display_event(self, session: Session, event: ClassroomEvent):
        self.ui.clear(session)
        text = event.get_full_details()
        buttons_list = [self.ui.create_button_view("מחק", lambda
            s: self.delete_event(s, event)),
                        self.ui.create_button_view("🔙",
                                                   self.view_classrooms)]
        self.ui.create_button_group_view(session,
                                         f"למחוק את האירוע הבא?\n{text}",
                                         buttons_list).draw()

    def delete_event(self, session: Session, event: ClassroomEvent):
        event.delete_self()
        self.ui.clear(session)
        finish_view = self.ui.create_text_view(session, "הזמנת הכיתה נמחקה")
        self.ui.summarize_and_close(session, views=[finish_view])

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
