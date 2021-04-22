from typing import Callable

from BotFramework.Activity.FormActivity.Field.field import Field
from BotFramework.View.view_container import ViewContainer


class TextField(Field[str]):
    """
    Field that allows the user to enter a free text
    """

    def __init__(self, name: str, msg: str, value: str = None):
        super().__init__(name, value)
        self.msg: str = msg

    def show_input_view(self, view_container: ViewContainer, update_callback: Callable[[], None], hide_callback: Callable[[], None]):
        super().show_input_view(view_container, update_callback, hide_callback)

        view_container.ui.create_text_view(view_container.session, self.msg, view_container).draw()
        view_container.ui.get_text(view_container.session, self.finish_input_view)
