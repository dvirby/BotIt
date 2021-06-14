from APIs.OtherAPIs import User
from APIs.OtherAPIs.Constraint.UserConstraint.user_constraint import MachzorConstraint, UserConstraint
from BotFramework.Activity.FormActivity.Field import TextField
from BotFramework.Activity.FormActivity.Field import CheckBoxField
from BotFramework.Activity.FormActivity.form_activity import FormActivity


class RemoveGroupParticipants:

    def __init__(self, group):
        users = UserConstraint.get_users_with_constraint(MachzorConstraint(User.mahzor))
        toAdd = []
        for u in users:
            if u in group:
                toAdd.append(u)

        self.AddedP = CheckBoxField(name="subtract", msg="Who do you want to remove?", options=toAdd)

    def validate(self):
        pass