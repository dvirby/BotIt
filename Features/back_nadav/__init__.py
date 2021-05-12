from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="corona updates", _type=FeatureType.REGULAR_FEATURE)
