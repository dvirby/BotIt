from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Main", _type=FeatureType.FEATURE_CATEGORY)
