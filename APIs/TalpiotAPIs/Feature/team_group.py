from __future__ import annotations
from mongoengine import *

from APIs.ExternalAPIs import GoogleSheets
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Group.commanded_group import CommandedGroup
from APIs.TalpiotAPIs.Group.division_group import DivisionGroup
from APIs.TalpiotAPIs.Group.role_group import RoleGroup
from APIs.TalpiotAPIs.Group.group import Group


class TeamGroup(CommandedGroup):
    division: DivisionGroup = ReferenceField(DivisionGroup)


if __name__ == '__main__':
    from settings import load_settings
    from APIs.TalpiotSystem import Vault

    load_settings()
    Vault.get_vault().connect_to_db()

    print(TeamGroup.objects[0].participants)

