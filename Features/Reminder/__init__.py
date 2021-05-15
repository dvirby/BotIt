from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="תזכורות",show_in_menu=True, _type=FeatureType.REGULAR_FEATURE,emoji="🗂")
