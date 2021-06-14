from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="My profile", _type=FeatureType.REGULAR_FEATURE, emoji = '👤')
