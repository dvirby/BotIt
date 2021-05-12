from __future__ import annotations
from enum import Enum
import os
from abc import ABC, abstractmethod


class OperationMode(Enum):
    DEVELOPMENT, TESTING, PRODUCTION = range(3)


class GoogleConnectionSettings(ABC):
    @abstractmethod
    def get_service(self, api_name: str, api_version: str, scopes: [str], token_file_path: str):
        pass


class GoogleConnectionSettingsPersonal(GoogleConnectionSettings):
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path

    def get_service(self, api_name: str, api_version: str, scopes: [str], token_file_path: str):
        from APIs.ExternalAPIs.Google.service_creator import get_google_service_personal

        return get_google_service_personal(
            api_name=api_name,
            api_version=api_version,
            scopes=scopes,
            credentials_file_path=self.credentials_path,
            token_file_path=token_file_path
        )


class GoogleConnectionSettingsServiceAccount(GoogleConnectionSettings):
    def __init__(self, service_account_key_path: str):
        self.service_account_key_path = service_account_key_path

    def get_service(self, api_name: str, api_version: str, scopes: [str], token_file_path: str):
        from APIs.ExternalAPIs.Google.service_creator import get_google_service

        return get_google_service(
            api_name=api_name,
            api_version=api_version,
            scopes=scopes,
            key_file_location=self.service_account_key_path
        )


class DatabaseSettings:
    def __init__(self, server_url: str,
                 server_port: int,
                 use_ssl: bool,
                 ssl_server_certificate: str,
                 authentication_table: str):
        self.server_url = server_url
        self.server_port = server_port
        self.use_ssl = use_ssl
        self.ssl_server_certificate = ssl_server_certificate
        self.authentication_table = authentication_table


class DatabaseCredentials:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class Settings:
    __instance = None

    def __init__(self,
                 database_creds: DatabaseCredentials,
                 database_settings: DatabaseSettings = DatabaseSettings(
                     server_url="localhost",
                     server_port=27017,
                     use_ssl=False,
                     ssl_server_certificate="",
                     authentication_table='admin'  # todo change name
                 ),
                 running_mode: OperationMode = OperationMode.DEVELOPMENT,
                 credentials_path: str = '.',
                 google_connection_settings: GoogleConnectionSettings = GoogleConnectionSettingsPersonal(
                     credentials_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                                   "ExternalAPIs", "Google",
                                                   "credentials.json")
                 )):

        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")

        self.database_creds = database_creds
        self.database_settings = database_settings
        self.running_mode: OperationMode = running_mode
        self.credentials_path: str = credentials_path
        self.google_connection_settings = google_connection_settings

        Settings.__instance = self

    @staticmethod
    def isSet() -> bool:
        if Settings.__instance is None:
            return False
        else:
            return True

    @staticmethod
    def get() -> Settings:
        if Settings.__instance is None:
            raise Exception("Settings are not set.")
        return Settings.__instance
