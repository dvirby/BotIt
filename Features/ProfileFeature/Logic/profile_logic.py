from APIs.OtherAPIs import User


class ProfileLogic:
    @staticmethod
    def get_user_description(user: User) -> [str]:
        messages = [
            '** username: **' + user.name,
            '** telegram ID: **' + str(user.telegram_id),
            '** E-Mail: **' + user.email
        ]

        return messages
