from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="create a new group", _type=FeatureType.REGULAR_FEATURE)
