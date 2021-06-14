from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="Reminders", show_in_menu=True,
                           _type=FeatureType.REGULAR_FEATURE, emoji="⏰")
