from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Examples", _type=FeatureType.FEATURE_CATEGORY, emoji='‍💻')
