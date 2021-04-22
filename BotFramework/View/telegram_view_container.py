from __future__ import annotations
import typing

from BotFramework.View.view_container import ViewContainer

if typing.TYPE_CHECKING:
    from BotFramework.session import Session
    from BotFramework.Telegram.telegram_ui import TelegramUI


class TelegramViewContainer(ViewContainer):
    def __init__(self, session: Session, ui: TelegramUI):
        super().__init__(session, ui)

        self.ui = ui
