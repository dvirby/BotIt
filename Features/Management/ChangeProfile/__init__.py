from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Change profile", _type=FeatureType.REGULAR_FEATURE)
