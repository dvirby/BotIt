from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="חיפוש אנשים", _type=FeatureType.REGULAR_FEATURE)
