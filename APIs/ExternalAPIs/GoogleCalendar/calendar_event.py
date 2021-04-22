from typing import Union, Optional
from datetime import datetime, date
from APIs.ExternalAPIs.GoogleCalendar.calendar_helper import iso_date_format


class CalendarEvent:
    def __init__(self, title: str,
                 start_time: Union[datetime, date],
                 end_time: Union[datetime, date],
                 location: Optional[str],
                 attendees: Optional[list]=None,
                 creator: dict=None,
                 calendar_event_id: str=None):
        """
        Creates a new CalendarEvent
        :param title:
        :param start_time:
        :param end_time:
        :param location:
        :param attendees:
        :param creator:
        :param calendar_event_id:
        """
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.attendees = attendees if attendees else []
        self.creator = creator
        self.calendar_event_id = calendar_event_id

    def get_data_dict(self) -> dict:
        """
        Returns dictionary representation of the object, fits to
        send to the Google Calendar API
        :return:
        """
        return {
            'summary': self.title,
            'start': CalendarEvent._get_date_dict(self.start_time),
            'end': CalendarEvent._get_date_dict(self.end_time),
            'attendees': list(map(lambda x: {"email": x.email}, self.attendees)),
            'location': self.location
        }

    def is_all_day(self) -> bool:
        """
        Checks if the event is all-day or not.
        :return: bool
        """

        return type(self.start_time) is date or type(self.end_time) is date

    @staticmethod
    def _get_date_dict(obj: Union[datetime, date]) -> dict:
        if type(obj) is datetime:
            return {'dateTime': iso_date_format(obj)}

        if type(obj) is date:
            return {'date': obj.isoformat()}

        return {}
