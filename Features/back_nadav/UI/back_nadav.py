from APIs.ExternalAPIs import *
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.ui.ui import UI
from APIs.OtherAPIs.DatabaseRelated.User.user import User
import covid19_data

hisID = ""
hisPwd = ""
hisSchool = ""
class back_nadav(BotFeature):

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
        buttons.append(self.ui.create_button_view("מספר המחלימים, המתים והמאומתים בכל העולם", self.world_data))
        buttons.append(self.ui.create_button_view("מספר המחלימים, המתים והמאומתים בישראל", self.Israel_data))
        self.ui.create_button_group_view(session, "איזה מידע בנוגע לקורונה אתה רוצה לראות?", buttons).draw()



    def world_data(self, session):
        total = covid19_data.dataByName("Total")
        self.ui.create_text_view(session, "מספר החולים שאומתו בעולם כרגע הוא:" + str(total.confirmed)).draw()
        self.ui.create_text_view(session, "מספר המתים בעולם כרגע הוא:" + str(total.deaths)).draw()
        self.ui.create_text_view(session, "מספר המחלימים בעולם כרגע הוא:" + str(total.recovered)).draw()


    def Israel_data(self, session):
        israel = covid19_data.dataByName("Israel")
        self.ui.create_text_view(session, "מספר החולים שאומתו בישראל כרגע הוא:" + str(israel.confirmed)).draw()
        self.ui.create_text_view(session, "מספר המתים בישראל כרגע הוא:" + str(israel.deaths)).draw()
        self.ui.create_text_view(session, "מספר המחלימים בישראל כרגע הוא:" + str(israel.recovered)).draw()




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
