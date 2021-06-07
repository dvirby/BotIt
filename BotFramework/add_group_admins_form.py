from APIs.OtherAPIs import User
from APIs.OtherAPIs.Constraint.UserConstraint.user_constraint import MachzorConstraint, UserConstraint
from BotFramework.Activity.FormActivity.Field import TextField
from BotFramework.Activity.FormActivity.Field import CheckBoxField
from BotFramework.Activity.FormActivity.form_activity import FormActivity


class AddGroupAdmins:

    def __init__(self, group):
        users = UserConstraint.get_users_with_constraint(MachzorConstraint(User.mahzor))
        toAdd = []
        for u in users:
            if u in group and u not in group.admins:
                toAdd.append(u)

        self.AddedA = CheckBoxField(name="add", msg="Who do you want to make admin?", options=toAdd)

    def validate(self):
        return True