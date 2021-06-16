import sys
import traceback
from typing import Callable

from BotFramework.UIbase.create_basic_ui import UI
import rstr
from BotFramework.session import Session

CODE_REGEX = r"^[a-zA-Z0-9]{8}$"
ERROR_OCCURRED_USER = "The feature has an error." + "\n" + "feature name: %s" + "\n" + "error id:" + " #%s"
ERROR_OCCURRED_ADMIN = "The feature has an error." + "\n" + "feature name: %s" + "\n" + "error id:" + " #%s" + "\n" + "the error: ```%s```"


class ErrorReport:
    """
    Holds information about a Crash of the
    bot. Has option to format the report
    for the user, and for an admin.
    """

    def __init__(self, session: Session, crash_log: str):
        self.report_id: str = rstr.xeger(CODE_REGEX)
        self.session: Session = session
        self.crash_log: str = crash_log

    def get_user_readable_text(self) -> str:
        return ERROR_OCCURRED_USER % (self.session.feature_name, self.report_id)

    def get_admin_readable_text(self) -> str:
        return ERROR_OCCURRED_ADMIN % (self.session.feature_name, self.report_id, self.crash_log)


def log_all_exceptions(function_to_call: Callable[[], None], session: Session, ui: UI):
    try:
        function_to_call()

    except:
        report = ErrorReport(session, traceback.format_exc())

        #  Send message according to the type of the user
        if session.user is not None and "admin" in session.user.role:
            ui.summarize_and_close(session,
                                   [ui.create_text_view(session, report.get_admin_readable_text())])
        else:
            ui.summarize_and_close(session,
                                   [ui.create_text_view(session, report.get_user_readable_text())])
