from BotFramework.session import Session
from Features.ManageGroups.Code.state import State


class GroupsCadetData:
    def __init__(self, user_session: Session, state: State = State.OMW):
        self.state: State = state
        self.session: Session = user_session
