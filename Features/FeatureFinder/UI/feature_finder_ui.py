from BotFramework import *
from APIs.ExternalAPIs import *
from Features.FeatureFinder.Logic.feature_finder_logic import FeatureFinderLogic
from Features.SystemFeatures.HierarchicalMenu.Code.menu_node import MenuNode
from APIs.TalpiotAPIs import *
from APIs.Database import *
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.ui.ui import UI, Button
from APIs.TalpiotAPIs.User.user import User

from Features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import HierarchicalMenu


class FeatureFinderUI(BotFeature):

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        self.ui.create_text_view(session, 'מה לחפש?').draw()
        self.ui.get_text(session, self.got_feature_name)

    def got_feature_name(self, session: Session, feature_name: str):
        feature_nodes: [MenuNode] = FeatureFinderLogic.get_all_features(
            HierarchicalMenu.get_instance(self.ui).root_node)

        #  Filter by user privileges
        def is_authorized_by_user(node: MenuNode):
            if node.type == FeatureType.REGULAR_FEATURE:
                obj: BotFeature = node.payload
                if not obj.is_authorized(session.user):
                    return False

            return True

        feature_nodes = list(filter(is_authorized_by_user, feature_nodes))

        data = {node.emoji + ' ' + node.display_name: node for node in feature_nodes}

        def try_again(s: Session) -> None:
            """
            This function call after the user press the try again button
            :return: None
            """
            self.ui.clear(s)
            self.main(s)

        self.ui.create_closest_name_view(session, data, feature_name, 5, self.got_feature,
                                         try_again).draw()

    def got_feature(self, session: Session, activity: ClosestNameActivity, feature_node: MenuNode):
        HierarchicalMenu.get_instance(self.ui).run_feature(session, feature_node.payload)

    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        pass

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "מתלם" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []
