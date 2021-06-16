from __future__ import annotations
from typing import TYPE_CHECKING

from BotFramework.UIbase.button import Button

if TYPE_CHECKING:
    from BotFramework.session import Session

class URL_button(Button):
    """
    Button class that can be used by views that require it
    """

    def __init__(self, title: str = "", func_to_call=(lambda: print("func to call not given")), url: str = None, *args,
                 **kwargs):
        super().__init__(title, func_to_call, *args, **kwargs)
        self.url = url



    def __eq__(self, other: Button):
        """Overrides the default implementation"""
        if isinstance(other, Button):
            return self.title == other.title and\
                   self.func_to_call == other.func_to_call and \
                   self.url == other.url and \
                   self.args == other.args and \
                   self.kwargs == other.kwargs

        return False

    def call_function(self, session: Session):
        self.func_to_call(session, *self.args, **self.kwargs)



