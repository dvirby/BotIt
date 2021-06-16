import datetime

from BotFramework import *
from APIs.ExternalAPIs import *
from APIs.OtherAPIs import *
from Features.ExamplesFeatures.Reminder.scheduled_action import scheduled_action
from Features.ExamplesFeatures.Reminder.UI.Reminder import Reminder
from Features.ExamplesFeatures.WashingMachine.DBModels.washing_machine_db import washing_machine_db
from Features.ExamplesFeatures.WashingMachine.DBModels.washing_machine_db import \
    washing_machine_settings
from Features.ExamplesFeatures.WashingMachine.Logic.washing_machine_logic import \
    washing_machine_logic


class washing_machine(BotFeature):
    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)
        if (len(washing_machine_db.objects) == 0):
            for name in washing_machine_settings.names:
                machine = washing_machine_db()
                machine.name = name
                machine.user = None
                machine.mode = None
                machine.remind = False
                machine.end_time = datetime.datetime.now()
                machine.save()

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """

        washing_machine_logic.restore(self, session)

        buttons = [
            self.ui.create_button_view("Use washing machine", lambda s: self.choose_name(session)),
            self.ui.create_button_view("get current washing machine report",
                                       lambda s: self.report(session))]
        self.ui.create_button_group_view(session, "What do you want to do?", buttons).draw()

    def report(self, session: Session):
        """show last report about the washing machine"""
        self.details = f"***Report washing machines {datetime.datetime.now().strftime('%Y-%m-%d, %H:%M')}***"
        if (len(washing_machine_db.objects) == 0):
            self.details += f"\n\n***No have washing machines to display***"
        else:
            for machine in washing_machine_db.objects:
                if (machine.name == None or washing_machine_logic().check_available(machine.name)):
                    self.details += f"\n\n***Washing machine name: {machine.name}***\n***Status: *** Available"
                else:
                    self.details += f"\n\n***Washing machine name: {machine.name}***\n***Status: *** Used\n***by: ***{machine.user.name}\n***until:*** {machine.end_time.strftime('%Y-%m-%d, %H:%M')}"
        self.ui.create_text_view(session, self.details).draw()
        self.ui.create_button_group_view(session, "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*", [
            self.ui.create_button_view("End", lambda s: self.ui.clear(session))]).draw()

    def choose_name(self, session: Session):
        """choose name method"""
        self.ui.clear(session)
        self.no_exict = True
        self.names = washing_machine_settings.names

        for name in self.names:
            if (washing_machine_logic().check_available(name)):
                self.no_exict = False

        if (self.no_exict):
            self.ui.create_text_view(session, "***No have available washing machines***").draw()
            self.ui.create_button_group_view(session, "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*", [
                self.ui.create_button_view("End", lambda s: self.ui.clear(session))]).draw()
        else:
            buttons = []
            for name in self.names:
                if (washing_machine_logic().check_available(name)):
                    buttons.append(self.ui.create_button_view(name, lambda s,
                                                                           value=name: self.choose_mode(
                        session, value)))
            self.ui.create_button_group_view(session,
                                             "Choose washing machine name from the availables",
                                             buttons).draw()

    def choose_mode(self, session: Session, name):
        """choose washing machine mode method"""
        self.ui.clear(session)
        buttons = []
        for mode in washing_machine_settings.modes.keys():
            buttons.append(self.ui.create_button_view(mode,
                                                      lambda s, value=mode: self.create_holding(
                                                          session, value, name)))
        self.ui.create_button_group_view(session, "Choose mode", buttons).draw()

    def create_holding(self, session: Session, mode, name):
        """before holding the washing machine set few properties"""
        self.ui.clear(session)
        self.ui.create_text_view(session,
                                 f"***Details***\n\n***Washing machine name:*** {name}\n***Mode:*** {mode}\n***Time duration:*** {washing_machine_settings.modes.get(mode) / 60} minutes").draw()
        buttons = [self.ui.create_button_view("Continue", lambda s: self.hold(session, mode, name)),
                   self.ui.create_button_view("Cancel", lambda s: self.ui.clear(session))]
        self.ui.create_button_group_view(session, "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*", buttons).draw()

    def hold(self, session: Session, mode, name):
        """create the final holding"""
        self.ui.clear(session)
        self.modes = washing_machine_settings.modes
        self.hold_time = datetime.datetime.now() + datetime.timedelta(0, self.modes[mode])
        if (washing_machine_logic().hold(name, mode, self.hold_time, session.user)):
            self.ui.create_text_view(session,
                                     f"***You're successfully holding the washing machine***").draw()
            self.hold_details = f"***From:*** {self.hold_time.strftime('%Y-%m-%d, %H:%M')}\n***Washing machine:*** {name}\n***Mode:*** {mode}\n***Time duration:*** {self.modes[mode] / 60}\n\n***FINISHED WASHING***"

            buttons = [self.ui.create_button_view("End & Create a reminder for a termination",
                                                  lambda s: self.create_remind(session,
                                                                               self.hold_time,
                                                                               self.hold_details,
                                                                               name)),
                       self.ui.create_button_view("End", lambda s: self.ui.clear(session))]
            self.ui.create_button_group_view(session, "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*",
                                             buttons).draw()
        else:
            self.ui.create_text_view(session,
                                     f"***We are so sorry but lately someone else take this washing machine\n***try again later").draw()
            self.ui.create_button_group_view(session, "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*", [
                self.ui.create_button_view("End", lambda s: self.ui.clear(session))]).draw()

    def create_remind(self, session: Session, hold_time, hold_details, name):
        self.ui.clear(session)
        washing_machine_db.objects(name=name)[0].remind = True
        scheduled_action.start_sync_action_by_date(hold_time,
                                                   lambda: Reminder.show_task(self, session,
                                                                              hold_details))

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
