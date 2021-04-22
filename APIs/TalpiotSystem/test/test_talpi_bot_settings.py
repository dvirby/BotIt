# import os
# import unittest
#
# from APIs.TalpiotSystem import TalpiotSettings, TALPI_BOT_PATH, TalpiotOperationMode, TalpiotDatabaseCredentials
#
#
# class TestSettings(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.settings = TalpiotSettings(TalpiotDatabaseCredentials("username", "password"))
#
#     def test_create_settings(self):
#         self.assertEqual(self.settings.database_settings.server_url, "talpibot.westeurope.cloudapp.azure.com")
#         self.assertEqual(self.settings.database_settings.server_port, 27018)
#         self.assertEqual(self.settings.database_settings.use_ssl, True)
#         self.assertEqual(self.settings.database_settings.authentication_table, "talpibot_main")
#
#         self.assertEqual(self.settings.running_mode, TalpiotOperationMode.DEVELOPMENT)
#         self.assertEqual(self.settings.database_creds.username, "username")
#         self.assertEqual(self.settings.database_creds.password, "password")
#
#
#     def test_get_settings(self):
#         self.assertEqual(self.settings, TalpiotSettings.get())
