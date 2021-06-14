from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Search Feature", _type=FeatureType.REGULAR_FEATURE, emoji='🔍')
