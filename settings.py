import os
from typing import Optional
from APIs.System import Settings, DatabaseCredentials, DatabaseSettings

"""
setting.py - a settings file for the system. The TalpiBotSettings is a singleton class.

In order to get the settings in your code you can use TalpiBotSettings.get()

For example:
    return TalpiBotSetting.get().database_creds.username
        
DO NOT UPLOAD YOUR SETTINGS FILE TO GIT.
"""


def get_bot_token() -> str:
    # return "1749704081:AAFeJUCAlaV4l8ssolWCEyGk0GPyWVIGHHU"
    return "1712673651:AAElBzlxroIATMsqEKv31DXYiujvkDrWzwM"


# todo change name
def get_credentials() -> DatabaseCredentials:
    return DatabaseCredentials(
        "dvirby",
        "123456789"
    )


def load_settings():
    # IMPORTANT: RUN THE FOLLOWING COMMAND BEFORE CHANGING THIS FILE:
    #
    #           git update-index --assume-unchanged settings.py
    #           git update-index --skip-worktree settings.py
    #
    # THIS WILL PREVENT YOUR SECRET CREDENTIALS FROM BEING UPLOADED TO THE MAIN REPO.
    Settings(database_creds=get_credentials(),
             database_settings=DatabaseSettings(
                 server_url="localhost",
                 server_port=27017,
                 use_ssl=False,
                 ssl_server_certificate='',
                 authentication_table='admin'
             ),
             )
