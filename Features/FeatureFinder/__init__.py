from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="חפש פיצ׳ר", _type=FeatureType.REGULAR_FEATURE, emoji='🔍')