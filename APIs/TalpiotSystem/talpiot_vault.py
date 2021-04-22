from __future__ import annotations
from typing import Dict
from mongoengine import connect, DEFAULT_CONNECTION_NAME as MONGOENGINE_DEFAULT_CONNECTION_NAME

from APIs.TalpiotSystem import TalpiotSettings, TBLogger


class Vault:
    __instance = None

    def __init__(self):

        if Vault.__instance is not None:
            raise Exception("This class is a singleton!")

        self._active_db_connections: Dict[str, bool] = dict()
        Vault.__instance = self

    @staticmethod
    def get_vault() -> Vault:
        if Vault.__instance is None:
            Vault()
        return Vault.__instance

    def connect_to_db(self, alias: str = MONGOENGINE_DEFAULT_CONNECTION_NAME):
        """
        Connects to a DB with the given alias. The alias of every db
        equals to the db name, except for the talpibot_main db that
        it's alias is "default"
        :param alias: The name of the DB or "default" for talpibot_main
        :return:
        """

        #  Check if this connection is not already open
        if alias in self._active_db_connections:
            return

        #  Get username&password from db
        settings = TalpiotSettings.get().database_settings
        database_creds = TalpiotSettings.get().database_creds

        #  Get real db name
        db_name = alias
        if alias == MONGOENGINE_DEFAULT_CONNECTION_NAME:
            db_name = "talpibot_main"

        #  Connect to the DB
        TBLogger.info("Connecting to db `%s` [%s]..." % (alias, db_name))

        connect(
            db=db_name,
            username=database_creds.username,
            password=database_creds.password,
            authentication_source=settings.authentication_table,
            host=settings.server_url,
            port=settings.server_port,
            ssl=settings.use_ssl,
            alias=alias
        )

        self._active_db_connections[alias] = True

