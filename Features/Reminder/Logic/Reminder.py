import sched, time, datetime
class ScheduledAction:

    def setTime(self, date):
        self.__date=date.time()

    def getTime(self):
        return self.__date.time()

    def setAction(self, action):
        self.__action=action

    def getAction(self, action ):
        return self.__action


    def createScheduledNotification(self):
        # Run 10 seconds from now
        # Create the scheduler
        s = sched.scheduler(self.__time.time)
        s.enterabs(self.__time.time, 1, self.__action)

        # Run the scheduler
        s.run()
        print("s.run() exited")