import locale
import os

from APIs.TalpiotSystem import Vault
from settings import load_settings


def fix_git():
    for line in open('GettingStarted/git_ignore.bat').readlines():
        os.system(line)


def run_setup():
    load_settings()
    fix_git()
    locale_setup()
    Vault.get_vault().connect_to_db()


def locale_setup():
    try:
        locale.setlocale(locale.LC_ALL, "he_IL.utf8")
    except:
        locale.setlocale(locale.LC_ALL, "he_IL")
