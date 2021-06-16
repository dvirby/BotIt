from APIs.OtherAPIs.Constraint.UserConstraint.user_constraint import UserConstraint, \
    MachzorConstraint
from BotFramework.Activity.FormActivity.Field import TextField
from BotFramework.Activity.FormActivity.form_activity import FormActivity
from BotFramework.Activity.FormActivity.Field import CheckBoxField
from APIs.OtherAPIs.DatabaseRelated.User.user import User


class CreateGroupForm:
    BAD_GROUP_NAME = "check your group name"
    BAD_DESCRIPTION = "check your description"
    BAD_PARTICIPANT = "check your participants"
    BAD_ADMINS = "check  your admins"

    def __init__(self):
        users = User.objects
        # check that fields are same in user.
        self.groupName = TextField(name="groupName", msg="What is your group name?")
        self.description = TextField(name="description", msg="What is the group description?")
        self.participants = CheckBoxField(name="participants", msg="Who will be in your group?",
                                          options=users)
        # self.admins = CheckBoxField(name="participants", msg="Who will be the admins of the group?", options=users)

    def validate(self):
        if self.groupName.value is None:
            raise FormActivity.ValidationException(self.BAD_GROUP_NAME)
        if self.description.value is None:
            raise FormActivity.ValidationException(self.BAD_DESCRIPTION)
        if self.participants is None:
            raise FormActivity.ValidationException(self.BAD_PARTICIPANT)

