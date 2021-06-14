from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Menu feature", _type=FeatureType.REGULAR_FEATURE, show_in_menu=False)
