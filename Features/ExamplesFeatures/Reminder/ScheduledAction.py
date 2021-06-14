import threading
from datetime import datetime

"""
class that enable to create tasks that will be run in a certain time
"""
class ScheduledAction:
    global __date
    global __action

    def  __init__(self,date:datetime,action):
        self.__date=date

    def set_date(self, date:datetime):
        self.__date = date

    def get_date(self):
        return self.__date

    def set_action(self, action):
        self.__action = action

    """the method will create scheduled action that run after delay(arg) seconds"""
    def create_sync_action_according_delay(self, delay):
        threading.Timer(delay,self.__action).start()

    def get_action(self):
        return self.__action



    """create the scheduled action by the date that determined in method set_date"""
    def create_sync_action(self):
        self.delay=(self.__date-datetime.datetime.now()).total_seconds()
        threading.Timer(self.delay,self.__action).start()
