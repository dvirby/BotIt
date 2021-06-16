from datetime import datetime

from APIs.OtherAPIs import User
from BotFramework import Session
from Features.ExamplesFeatures.Reminder.UI.Reminder import Reminder
from Features.ExamplesFeatures.Reminder.scheduled_action import scheduled_action
from Features.ExamplesFeatures.WashingMachine.DBModels.washing_machine_db import washing_machine_db, washing_machine_settings


class washing_machine_logic:
    _restore: bool = False

    def check_available(self,name:str) -> bool:
        """checking if washing machine in used"""
        washing_machine=washing_machine_db.objects(name=name)
        for machine in washing_machine:
            if (machine.end_time==None or machine.end_time<datetime.now()):
                return True
        return False

    def restore(self,session:Session):
        if not washing_machine_logic._restore:
            self.modes = washing_machine_settings.modes
            for machine in washing_machine_db.objects(user=session.user):
                self.hold_time = machine.end_time
                if (self.hold_time > datetime.now() and machine.remind):
                    print("dp it")
                    self.hold_details = f"***From:*** {self.hold_time.strftime('%Y-%m-%d, %H:%M')}\n***Washing machine:*** {machine.name}\n***Mode:*** {machine.mode}\n***Time duration:*** {self.modes[machine.mode] / 60}\n\n***FINISHED WASHING***"
                    scheduled_action.start_sync_action_by_date(self.hold_time,
                                                               lambda: Reminder.show_task(self, session,
                                                                                          self.hold_details))
            washing_machine_logic._restore=True


    def hold(self,name:str,mode:str,end_time:datetime, user:User)-> bool:
        """catching the washing machine to use"""
        if(not self.check_available(name)):
            return False
        washing_machine=washing_machine_db.objects(name=name)[0]
        washing_machine.user = user
        washing_machine.mode = mode
        washing_machine.remind = False
        washing_machine.end_time = end_time
        washing_machine.save()
        return True

