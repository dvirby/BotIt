from __future__ import annotations
from mongoengine import *

from APIs.ExternalAPIs import GoogleSheets
from APIs.TalpiotAPIs.User.user import User


class Group(Document):
    meta = {'collection': 'groups', 'allow_inheritance': True, 'auto_create_index': False}

    name: str = StringField(max_length=100, required=True)
    description: str = StringField(max_length=100, required=True)
    participants: [User] = ListField(ReferenceField(User), required=True)
    admins: [User] = ListField(ReferenceField(User), required=True)

    def __repr__(self):
        return self.name

    def __contains__(self, user: User) -> bool:
        """
        This method checks if a user is in a certain group.
        Usage: if my_user in group: do something
        Args:
            user: the user object to check

        Returns: true iff the user is in the group.

        """
        return user in self.participants
