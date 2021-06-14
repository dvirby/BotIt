from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Management", _type=FeatureType.FEATURE_CATEGORY, emoji='⚙')
