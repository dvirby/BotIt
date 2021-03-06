from abc import abstractmethod

from BotFramework.View.BaseComponents.drawable import Drawable
from BotFramework.session import Session
from BotFramework.View.BaseComponents.view_container import ViewContainer


class View(Drawable):

    def __init__(self, view_container: ViewContainer):
        """
        Create a view that will be drawn using the given UI and belong to the given session
        :param UIbase: UIbase to draw the view on when draw() is called
        :param session: session this view belongs to
        """

        self.view_container = view_container
        self.sent = False

    def get_session(self) -> Session:
        return self.view_container.session

    def draw(self):
        """
        Draw this view on the UIbase
        """

        if self.is_sent():
            return False

        self.view_container.views.append(self)
        self.sent = True

        return True

    def update(self, *params):
        """
        update the view with new parameters
        :param params: new parameters (i.e new text for text_view).
        """
        if not self.is_sent():
            raise Exception("View updated before drawn. Use view.draw() first.")

    def is_sent(self):
        """
        Check if this view was drawn already
        :return: True if this view was drawn, False otherwise.
        """
        return self.sent

    def remove(self) -> bool:
        """
        Remove this view from the session and from the UIbase
        :return: True if the removal succeeded and False otherwise.
        """
        if not self.is_sent():
            return False

        try:
            self.remove_raw()
        except:
            pass

        self.view_container.views.remove(self)
        self.sent = False

        return True

    @abstractmethod
    def remove_raw(self):
        """
        Remove the actual message from the UIbase. subclass responsibility.
        """
        pass
