from BotFramework import FeatureSettings, FeatureType
from Features.SystemFeatures.Start.Code.start import Start


def get_settings():
    return FeatureSettings(display_name="Start", _type=FeatureType.REGULAR_FEATURE, show_in_menu=False)
