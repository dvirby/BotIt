from APIs.ExternalAPIs import GoogleCalendar
from Features.Classrooms.DBModels.classroom import *
from Features.Classrooms.DBModels.classroom_event import *
from datetime import datetime

class_list = ["ב'1", "ב'2", "ב'4", "ב'6", "ב'7", "ב'8", "ג'3",
              "חדר דיונים", "כיתת כיבוד", "אודיטוריום", "חדר מנחים"]
short_name_list = ["ב'1", "ב'2", "ב'4", "ב'6", "ב'7", "ב'8", "ג'3",
                   "חד\"ן", "כיבוד", "אודיט'", "מנחים"]


def reset_classroom_db():
    for classroom in Classroom.objects:
        classroom.delete()
    for i in range(len(class_list)):
        classroom = Classroom()
        classroom.name = class_list[i]
        classroom.short_name = short_name_list[i]
        classroom.save()


def reset_event_db(_date):
    for event in ClassroomEvent.objects:
        try:
            if event.classroom not in Classroom.objects:
                event.classroom = Classroom.objects[0]
                event.save()
            event.delete_self()
        except:
            continue
