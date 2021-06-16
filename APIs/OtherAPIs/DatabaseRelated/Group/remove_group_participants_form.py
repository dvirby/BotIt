from APIs.OtherAPIs import User
from APIs.OtherAPIs.Constraint.UserConstraint.user_constraint import MachzorConstraint, \
    UserConstraint
from BotFramework.Activity.FormActivity.Field import CheckBoxField


class RemoveGroupParticipants:

    def __init__(self, group):
        users = User.objects
        toAdd = []
        for u in users:
            if u in group:
                toAdd.append(u)

        self.AddedP = CheckBoxField(name="remove", msg="Who do you want to remove?", options=toAdd)

    def validate(self):
        pass
