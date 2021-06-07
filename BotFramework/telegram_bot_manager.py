import logging
from typing import Union, Dict, Type
import telegram

from BotFramework.bot_user import BotUser
from telegram.update import Update
from telegram.ext import Updater, Filters, CallbackContext
from telegram.ext import messagequeue as mq
from telegram.ext import MessageHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.request import Request
from BotFramework.bot_manager import BotManager
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.telegram_queued_bot import TelegramQueuedBot
from BotFramework.telegram_ui import TelegramUI
from BotFramework.crash_logger import log_all_exceptions
from BotFramework.session import Session
from BotFramework.bot_logger import BotLogger
from APIs.OtherAPIs.DatabaseRelated.User.user_detailes_form import UserDetailesForm
from BotFramework.Activity.FormActivity.form_activity import FormActivity
from APIs.OtherAPIs.DatabaseRelated import User

class TelegramBotManager(BotManager):
    def __init__(self, token: str, user_type: Type[BotUser]):
        self.token = token

        # init global bot objects
        self.updater: telegram.ext.updater.Updater = None
        self.dispatcher = None
        self.raw_api_bot: telegram.bot.Bot = None

        # connect the bot to the token
        self.connect_to_token(token)
        self.load_handlers()

        # custom feature list
        self._custom_features = dict()

        # todo solve this error (self.dispatcher is None)
        self.user_type = user_type

        self.ui = TelegramUI(self.raw_api_bot, self.dispatcher, self.user_type)
        self.features: Dict[str, BotFeature] = dict()

        # init logger
        self.logger: Union[logging.Logger, logging.RootLogger] = None
        self.init_logger()

    def load_handlers(self):
        """
        Create handler for getting commands. Handlers for text, images and buttons are UI responsibility
        """
        commands_handler = MessageHandler(Filters.command, self.command_handler)
        self.dispatcher.add_handler(commands_handler)

    def run(self):
        """
        Start the bot and make it receive messages.
        """
        # Start the Bot
        self.updater.start_polling()

        BotLogger.success("Bot started running.")
        BotLogger.success("You can now open telegram and use it.")

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def connect_to_token(self, token):
        """
        Create a connection to the telegram token with the given token
        :param token: telegram bot token to connect to
        """
        q = mq.MessageQueue(all_burst_limit=29, all_time_limit_ms=1000)

        # set connection pool size for bot
        request = Request(con_pool_size=8)

        # create a temp bot with a queue
        temp_bot = TelegramQueuedBot(token, request=request, mqueue=q)

        self.updater = telegram.ext.updater.Updater(bot=temp_bot, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.raw_api_bot: telegram.bot.Bot = self.updater.bot

    def init_logger(self):
        """
        Initialize the bot logger
        :return:
        """
        # Enable logging
        logging.basicConfig(format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def func1(self, session: Session, form_activity: FormActivity, form: UserDetailesForm):
        user = self.user_type.get_by_telegram_id(session.user.telegram_id)
        user.email = str(form.eMail.value)
        user.name = str(form.name.value)
        user.save()
        if form.is_admin.value == ['yes']:
            self.ui.create_text_view(session,"What is the admin password?").draw()
            self.ui.get_text(session, self.passwordCorrect)
        else:
            self.ui.create_text_view(session, "You are registered!").draw()

    def passwordCorrect(self, session, text):
        if str(text) == '123456789':
            user = self.user_type.get_by_telegram_id(session.user.telegram_id)
            user.role.append('bot_admin')
            self.ui.create_text_view(session, "You are registered as admin!").draw()
        else:
            self.ui.create_text_view(session, "Wrong password!").draw()

    @run_async
    def command_handler(self, update: Update, context: CallbackContext):
        if update.message.text == '/register':

            try:
                user = self.user_type.get_by_telegram_id(update.effective_user.id)
                session = self.ui.create_session("register", user)
                self.ui.create_text_view(session, "You are already registered! press /list").draw()
            except:
                user = User()
                user.telegram_id = update.effective_chat.id
                user.save()
                session = self.ui.create_session("register", user)
                self.ui.create_form_view(session, UserDetailesForm(), "please insert the following details:",
                                         self.func1).draw()

        """
        A message handler for getting commands
        """
        if '/start' in update.message.text:
            session = self.ui.create_session("start", None)
            from Features.SystemFeatures.Start import Start
            msg = update.message.text
            if len(msg.split()) >= 2:
                code = msg.split()[1]
                feature = Start(self.ui)

                session.data['secret_code'] = code
                session.data['telegram_id'] = update.effective_user.id

                log_all_exceptions(
                    lambda: feature.main(session),
                    session,
                    self.ui
                )

            return
        user = self.user_type.get_by_telegram_id(update.effective_user.id)
        if user is None:
            print(f"UNKNOWN ID: {update.effective_user.id}")
            raise Exception("ERROR - USER IS NONE" + f"UNKNOWN ID: {update.effective_user.id}")

        if update.message.text == '/list':
            from Features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import HierarchicalMenu
            self.raw_api_bot.delete_message(user.telegram_id, update.message.message_id)

            HierarchicalMenu.run_menu(self.ui, user)

        if update.message.text in self._custom_features:
            self.ui.clear_feature_sessions_user(update.message.text, user)
            session = self.ui.create_session(update.message.text, user)

            self.raw_api_bot.delete_message(user.telegram_id, update.message.message_id)
            self.ui.create_text_view(session, "אתה מריץ פקודה במצב טסטים.").draw()
            feature = self._custom_features[update.message.text]

            log_all_exceptions(
                lambda: feature.main(session),
                session,
                self.ui
            )
