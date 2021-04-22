import unittest
from unittest.mock import MagicMock

from BotFramework import TelegramUI, Session
from BotFramework.View.telegram_image_view import TelegramImageView
from BotFramework.test.mock_container import MockContainer
from BotFramework.test.test_bot_user import TestBotUser



class TestTelegramContactView(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        bot = MockContainer()
        bot.send_photo = MagicMock()
        bot.send_message = MagicMock()
        bot.send_contact = MagicMock()

        dispatcher = MockContainer()
        dispatcher.add_handler = MagicMock()

        cls.ui = TelegramUI(bot, dispatcher, TestBotUser)
        cls.user = TestBotUser(telegram_id='id_test', id="123")
        cls.session = cls.ui.create_session("Testing", cls.user)

    def test_draw(self):
        view = TelegramImageView(self.session.view_container, "test_image", "test.png")
        view.draw()

        args, kwargs = self.ui.raw_bot.send_photo.call_args
        self.assertEqual(args[0], self.session)
        self.assertEqual(args[1], self.user.telegram_id)
        self.assertEqual(kwargs["caption"], "test_image")

    def test_update(self):
        view = TelegramImageView(self.session.view_container, "test_image", "test.png")
        view.draw()

        view.raw_object.result().edit_text = MagicMock()
        view.update("updated", "update.png")
        args, kwargs = view.raw_object.result().edit_caption.call_args
        self.assertEqual(kwargs["caption"], "updated")

    def test_delete(self):
        view = TelegramImageView(self.session.view_container, "test_image", "test.png")
        view.draw()

        view.raw_object.result().delete = MagicMock()

        temp = view.raw_object
        view.remove()
        temp.result().delete.assert_called_with()