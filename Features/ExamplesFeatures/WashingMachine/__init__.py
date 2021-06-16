from datetime import datetime

from BotFramework import FeatureSettings, FeatureType
from Features.ExamplesFeatures.WashingMachine.DBModels import washing_machine_db
from Features.ExamplesFeatures.WashingMachine.DBModels.washing_machine_db import washing_machine_settings


def get_settings():
    return FeatureSettings(display_name="Washing machine", _type=FeatureType.REGULAR_FEATURE, emoji = '🧺')

