import threading
from BotFramework import *
from APIs.ExternalAPIs import *
from APIs.OtherAPIs import *


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






    def choose_date(self, view,  session: Session, date:datetime):
        global date_time
        date_time = str(date).split(",")[0]
        self.ui.clear(session)
        self.ui.create_time_choose_view(session, self.choose_time).draw()




    def choose_time(self, view,  session: Session, time:datetime):

        global day_time
        day_time = str(time).split(" ")[1][0:5]
        self.get_msg(session)


    def get_msg(self,  session: Session):
        self.ui.clear(session)
        self.ui.create_text_view(session, "***Enter text to remind***").draw()
        self.ui.get_text(session, self.create_reminder)


    def create_reminder(self, session: Session, text):
        self.ui.clear(session)
        global msg
        msg = text
        buttons = []
        buttons.append(self.ui.create_button_view("Cancel", lambda s: self.ui.clear(session)))

        date_time_str = date_time+", "+day_time


        buttons.append( self.ui.create_button_view("Save",lambda s:self.create_task(session,text,date_time_str)))
        self.ui.create_text_view(session,"The ***reminder*** will be remembered at \n***"+date_time_str+"***\n***Contect:***\n"+text).draw()
        self.ui.create_button_group_view(session, "*-*-*-*-*-*-*-*-*-*-*", buttons).draw()

    def create_task(self,session:Session,text,date_time_str):
        self.ui.clear(session)
        self.delay=(datetime.datetime.strptime(date_time_str, '%Y-%m-%d, %H:%M')-datetime.datetime.now()).total_seconds()
        threading.Timer(self.delay,lambda :self.show_task(session, text,date_time_str)).start()

    def show_task(self,session:Session,text,date_time_str):
        self.ui.create_text_view(session, "***Reminder***\n"+date_time_str+"\n***Contect:***\n"+text).draw()
        buttons=[]
        buttons.append(self.ui.create_button_view("Got it", lambda s: self.ui.clear(session)))
        self.ui.create_button_group_view(session,"*-*-*-*-*-*-*-*",buttons).draw()



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