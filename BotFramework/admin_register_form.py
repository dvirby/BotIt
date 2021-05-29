from BotFramework.Activity.FormActivity.Field import TextField
from BotFramework.Activity.FormActivity.form_activity import FormActivity


class AdminRegisterForm:
    BAD_USERNAME = "check your username"
    BAD_PASSWORD = "check your password"

    def __init__(self):
        # check that fields are same in user.
        self.username = TextField(name="username", msg="What is your username?")
        self.password = TextField(name="password", msg="What is your password?")

    def validate(self):
        if self.username.value is None:
            raise FormActivity.ValidationException(AdminRegisterForm.BAD_EMAIL)

        if self.password.value is None:
            raise FormActivity.ValidationException(AdminRegisterForm.BAD_NAME)
