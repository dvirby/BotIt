from APIs.OtherAPIs import User
from APIs.OtherAPIs.Constraint.UserConstraint.user_constraint import MachzorConstraint, UserConstraint
from BotFramework.Activity.FormActivity.Field import TextField
from BotFramework.Activity.FormActivity.Field import CheckBoxField
from BotFramework.Activity.FormActivity.form_activity import FormActivity


class RemoveGroupAdmins:

    def __init__(self, group):
        users = User.objects
        toAdd = []
        for u in users:
            if (u in group and u in group.admins) and 'bot_admin' not in u.role:
                toAdd.append(u)

        self.AddedA = CheckBoxField(name="add", msg="What admins do you want to make not admins?", options=toAdd)

    def validate(self):
        pass