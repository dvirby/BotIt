from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Manage groups", _type=FeatureType.REGULAR_FEATURE)
