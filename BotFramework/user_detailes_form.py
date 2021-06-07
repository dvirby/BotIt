from BotFramework.Activity.FormActivity.Field import TextField
from BotFramework.Activity.FormActivity.Field import CheckBoxField
from BotFramework.Activity.FormActivity.form_activity import FormActivity


class UserDetailesForm:
    BAD_EMAIL = "check your email"
    BAD_NAME = "check your name"

    def __init__(self):
        # check that fields are same in user.
        self.eMail = TextField(name="email", msg="What is your E-mail?")
        self.name = TextField(name="name", msg="What is your name?")
        self.is_admin = CheckBoxField(name="admin", msg="Are you admin?",options=['yes'])

    def validate(self):
        if self.eMail.value is None:
            raise FormActivity.ValidationException(UserDetailesForm.BAD_EMAIL)

        if self.name.value is None:
            raise FormActivity.ValidationException(UserDetailesForm.BAD_NAME)