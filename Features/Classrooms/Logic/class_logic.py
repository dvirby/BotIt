from APIs.ExternalAPIs import GoogleCalendar
from Features.Shagmach.Classrooms.DBModels.classroom import *
from Features.Shagmach.Classrooms.DBModels.classroom_event import *
from datetime import datetime

CALENDAR_ID = 'eeqbp1vhv9d4t7gc0liu4fktq8@group.calendar.google.com'

class_list = ["ב'1", "ב'2", "ב'4", "ב'6", "ב'7", "ב'8", "ג'3",
              "חדר דיונים", "כיתת כיבוד", "אודיטוריום", "חדר מנחים"]
short_name_list = ["ב'1", "ב'2", "ב'4", "ב'6", "ב'7", "ב'8", "ג'3",
                   "חד\"ן", "כיבוד", "אודיט'", "מנחים"]


def get_datetimes(date: str, hours: list) -> tuple:
    start_hour_text = date + hours[0]
    finish_hour_text = date + hours[1]
    start_time = datetime.strptime(start_hour_text, ' %a\' - %d/%m/%y %H:%M')
    finish_time = datetime.strptime(finish_hour_text, ' %a\' - %d/%m/%y %H:%M')
    date = datetime.strptime(date, ' %a\' - %d/%m/%y')
    return start_time, finish_time, date


def create_event(date: date, hours: list, user: User, classroom: Classroom):
    class_event = ClassroomEvent()
    class_event.classroom = classroom
    class_event.start_time = hours[0]
    class_event.end_time = hours[1]
    class_event.user = user
    class_event.date = date
    class_event.calendar = None
    create_calendar(class_event)
    class_event.save()


def get_free_classes(date: date, datetimes: list, classroom: Classroom):
    classroom_list = ClassroomEvent.objects(classroom=classroom, date=date)
    if classroom.short_name in ["ב'6", "ב'7", "ב'8"]:
        return False
    for event in classroom_list:
        if datetimes[0] <= event.start_time < datetimes[1] or datetimes[
            0] < event.end_time <= datetimes[1] or event.start_time <= datetimes[
            0] < event.end_time or event.start_time < datetimes[
            1] <= event.end_time:
            return False
    return True


def create_calendar(event: ClassroomEvent):
    cl_event = CalendarEvent(title=event.get_title(),
                             start_time=event.start_time,
                             end_time=event.end_time,
                             location=event.classroom.name,
                             attendees=[event.user])
    with GoogleCalendar.get_instance() as gc:
        cl_event = gc.insert_event(CALENDAR_ID, cl_event)
        event.calendar = cl_event.calendar_event_id