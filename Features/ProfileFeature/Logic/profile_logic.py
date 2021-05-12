from APIs.OtherAPIs import User


class ProfileLogic:
    @staticmethod
    def get_user_description(user: User) -> [str]:
        messages = [
            #בשביל שזה יעבוד צריך להגדיר בקוד את מספר הטלפון והמחזור.
            '** שם משתמש: **' + user.name,
            '** מספר פלאפון: **' + str(user.phone_number),
            '** כתובת מייל: **' + user.email,
            '** מחזור:**' + str(user.mahzor)
        ]

        return messages
