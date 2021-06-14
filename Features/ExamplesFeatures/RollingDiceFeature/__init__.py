from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Throw a cube", _type=FeatureType.REGULAR_FEATURE,
                           emoji='🎲')
