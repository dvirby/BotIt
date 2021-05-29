from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Create new group", _type=FeatureType.REGULAR_FEATURE)
