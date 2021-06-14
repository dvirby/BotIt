from __future__ import annotations
import datetime

from mongoengine import *
from enum import Enum



class Gender(Enum):
    male = "male"
    female = "female"
    other = "other"


class User(Document):
    meta = {'collection': 'users_info'}
    email: str = StringField()
    name: str = StringField(max_length=100)
    gender: str = StringField(max_length=10)
    phone_number: str = StringField()
    telegram_id: int = LongField()
    birthday: datetime.date = DateField()
    role: [str] = ListField(default=["מתלם"])
    secret_code: str = StringField()

    @staticmethod
    def get_by_telegram_id(telegram_id: int):
        return User.objects.get(telegram_id=telegram_id)

    def get_first_name(self) -> str:
        """
        Returns the first name of the user.

        :return:
        """
        return self.name.split(' ')[0]

    def get_last_name(self):
        """
        Returns the last name of the user.

        :return:
        """
        return self.name.split(' ')[-1]

    def get_short_name(self):
        """
        Returns first + last name of the user.

        :return:
        """

        return self.get_first_name() + " " + self.get_last_name()

    def get_gender(self):
        return Gender[self.gender]

    def get_team(self) -> [User]:
        if self.team_commander is None:
            return []

        return User.objects(
            team_commander=self.team_commander,
            mahzor=self.mahzor
        )

    def update_special_attribute(self, key, value):
        """
        Updates the special attributes, in the specific
        key specified, And then updates the database.

        :param key: The key to update
        :param value: The new value
        :return:
        """

        self.special_attributes[key] = value
        self.save()

    def get_special_attribute(self, key):
        """
        Returns the special attribute with the given key.

        :param key: The key to retrieve
        :return:
        """
        try:
            return self.special_attributes[key]
        except KeyError:
            return None

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.id)


if __name__ == "__main__":
    from settings import load_settings
    from APIs.System import Vault
    load_settings()
    Vault.get_vault().connect_to_db()
    u = User()
    u.email = "nadav.mihov@gmail.com"
    u.name = "nadav"
    u.role = ["מתלם","חנתר"]
    u.telegram_id = 2134546368
    u.save()
    print(User.objects)
