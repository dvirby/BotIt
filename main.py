from BotFramework import *
import GettingStarted.configuration_setup as ConfigSetup
import settings
from APIs.TalpiotAPIs import User


def get_bot_manager() -> BotManager:

    return TelegramBotManager(settings.get_bot_token(), User)


def main():
    ConfigSetup.run_setup()

    bm: BotManager = get_bot_manager()
    bm.run()


if __name__ == '__main__':
    main()
