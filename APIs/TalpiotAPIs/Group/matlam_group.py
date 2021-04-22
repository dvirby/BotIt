from __future__ import annotations
from mongoengine import *

from APIs.TalpiotAPIs import Group


class MatlamGroup(Group):
    pass

if __name__ == '__main__':
    from settings import load_settings
    from APIs.TalpiotSystem import Vault

    load_settings()
    Vault.get_vault().connect_to_db()

    print(Group.objects[0].participants)

