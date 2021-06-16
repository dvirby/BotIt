import datetime
from mongoengine import *
from APIs.OtherAPIs import User


class washing_machine_settings():
    names = ["Washing machine 1", "Washing machine 2", "Washing machine 3"]
    modes = {'Fast': 300, 'Normal': 600, 'Slow': 1200}


class washing_machine_db(Document):
    meta = {'collection': 'washing_machine'}
    user: User = ReferenceField(User, required=False)
    name:str = StringField(required=True)
    mode: str = StringField(required=False)
    end_time: datetime = DateTimeField(required=True)
    remind:bool= BooleanField(required=False)






