from typing import Type
from abc import ABC
from abc import abstractmethod
from BotFramework.Feature.bot_feature import BotFeature


class BotManager(ABC):
    @abstractmethod
    def load_handlers(self):
        pass

    @abstractmethod
    def run(self):
        pass
