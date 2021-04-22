from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BotFramework.telegram_ui import TelegramUI
from BotFramework.View.telegram_view_container import TelegramViewContainer

from BotFramework.session import Session
from BotFramework.bot_user import BotUser


class TelegramSession(Session):
    def __init__(self, feature_name: str, user: BotUser, telegram_ui: TelegramUI):
        super().__init__(feature_name, user, telegram_ui)

        self.view_container: TelegramViewContainer = TelegramViewContainer(self, telegram_ui)

if __name__ == "__main__":
    TelegramSession("", "", "")
