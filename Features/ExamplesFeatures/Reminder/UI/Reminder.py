from BotFramework import *
from APIs.ExternalAPIs import *
from APIs.OtherAPIs import *
from Features.ExamplesFeatures.Reminder.scheduled_action import scheduled_action



class Reminder(BotFeature):


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

        self.ui.create_date_choose_view(session, self.choose_date).draw()


    def choose_date(self, view:DateChooseView,  session: Session,chosen):
        """choose date"""
        self.ui.clear(session)
        self.ui.create_time_choose_view(session,lambda v,s,d:self.choose_time(s,datetime.datetime.combine(chosen,d.time()))).draw()

    def choose_time(self,  session: Session, chosen ):
        """choose time"""
        self.ui.clear(session)
        self.get_msg(session,chosen)


    def get_msg(self,  session: Session,chosen):
        """get message to show"""
        self.ui.clear(session)
        self.ui.create_text_view(session, "***Enter text to remind***").draw()
        self.ui.get_text(session, lambda s,t:self.create_reminder(s,t,chosen))


    def create_reminder(self, session: Session, text,chosen):
        """set lase properties"""
        self.ui.clear(session)
        buttons = [self.ui.create_button_view("Cancel", lambda s: self.ui.clear(session)),
                   self.ui.create_button_view("Save",lambda s:self.create_task(session,text,chosen))]
        self.ui.create_text_view(session,"The ***reminder*** will be remembered at \n***"+chosen.strftime('%Y-%m-%d, %H:%M')+"***\n***Contect:***\n"+text).draw()
        self.ui.create_button_group_view(session, "*-*-*-*-*-*-*-*-*-*-*", buttons).draw()


    def create_task(self,session:Session,text,chosen):
        """create the task"""
        self.ui.clear(session)
        text+='\nfrom: '+chosen.strftime('%Y-%m-%d, %H:%M')
        scheduled_action.start_sync_action_by_date( chosen,lambda s: self.show_task(session, text))


    def show_task(self,session:Session,text):
        """show the task"""
        self.ui.create_text_view(session, f"***Reminder***\n***Contect:***\n\n"+text).draw()
        self.ui.create_button_group_view(session,"*-*-*-*-*-*-*-*",[self.ui.create_button_view("Got it", lambda s: self.ui.clear(session))]).draw()



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
        return "reg_user" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []