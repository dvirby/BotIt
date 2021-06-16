import threading
from collections import Callable
import datetime

from BotFramework import Session

"""
class that enable to create tasks that will be run in a certain time
"""
class scheduled_action:

    def start_sync_action_by_timer( delay:int, action: Callable):
        """create the scheduled action by delay (in seconds)"""
        threading.Timer(delay,action).start()

    def start_sync_action_by_date(date:datetime, action: Callable):
        """create the scheduled action by date"""
        delay=(date-datetime.datetime.now()).total_seconds()
        scheduled_action.start_sync_action_by_timer(delay, action)

