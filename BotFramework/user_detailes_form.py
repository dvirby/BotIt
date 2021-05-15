from BotFramework.Activity.FormActivity.Field import TextField
from BotFramework.Activity.FormActivity.form_activity import FormActivity


class UserDetailesForm:
    BAD_EMAIL = "check your email"
    BAD_NAME = "check your name"

    def __init__(self):
        self.eMail = TextField(name="E-mail", msg="What is your E-mail?")
        self.name = TextField(name="Name", msg="What is your name?")

    def validate(self):
        if self.eMail.value is None:
            raise FormActivity.ValidationException(UserDetailesForm.BAD_EMAIL)

        if self.name.value is None:
            raise FormActivity.ValidationException(UserDetailesForm.BAD_NAME)
