from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Find contacts", _type=FeatureType.REGULAR_FEATURE,
                           emoji='☎')
