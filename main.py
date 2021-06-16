from BotFramework import *
import GettingStarted.configuration_setup as ConfigSetup
import settings
from APIs.OtherAPIs import User


def get_bot_manager() -> BotManager:
    return BotManager(settings.get_bot_token(), User)


def main():
    ConfigSetup.run_setup()

    bm: BotManager = get_bot_manager()
    bm.run()


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")
    main()
