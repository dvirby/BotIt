from APIs.OtherAPIs.Constraint.UserConstraint.user_constraint import UserConstraint, \
    MachzorConstraint
from APIs.OtherAPIs.DatabaseRelated.Group import groups_api
from BotFramework.Activity.FormActivity.form_activity import FormActivity
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.UIbase.create_basic_ui import UI
from APIs.OtherAPIs.DatabaseRelated.User.user import User
from APIs.OtherAPIs.DatabaseRelated.Group.group import Group
from APIs.OtherAPIs.DatabaseRelated.Group.add_group_participants_form import AddGroupParticipants
from APIs.OtherAPIs.DatabaseRelated.Group.add_group_admins_form import AddGroupAdmins
from APIs.OtherAPIs.DatabaseRelated.Group.remove_group_admins_form import RemoveGroupAdmins
from APIs.OtherAPIs.DatabaseRelated.Group.remove_group_participants_form import \
    RemoveGroupParticipants


class ManageGroups(BotFeature):

    def __init__(self, ui: UI):
        """
        Create a new vidutz module instance
        :param ui: UI instance to be used
        """
        super().__init__(ui)

    group2 = Group

    def main(self, session: Session) -> None:
        """
        Called when the /vidutz command is received. Initialized a VidutzData and send vidutz messages.
        :param session: The caller's session object
        """
        buttons = []
        for group in groups_api.get_user_groups(session.user):
            if session.user in group.admins:
                buttons.append(self.ui.create_button_view(group.name,
                                                          lambda s: self.show_small_menu(group,
                                                                                         session)))
        self.ui.create_button_group_view(session, "What group do you want to change?",
                                         buttons).draw()

    def show_small_menu(self, group: Group, session: Session):
        global group2
        group2 = group
        buttons = []
        buttons.append(self.ui.create_button_view("Change group name",
                                                  lambda s: self.change_name(group, session)))
        buttons.append(self.ui.create_button_view("Change group description",
                                                  lambda s: self.change_description(group,
                                                                                    session)))
        buttons.append(self.ui.create_button_view("Add participants",
                                                  lambda s: self.add_participants(group, session)))
        buttons.append(self.ui.create_button_view("remove participants",
                                                  lambda s: self.remove_participants(group,
                                                                                       session)))
        buttons.append(
            self.ui.create_button_view("Add admins", lambda s: self.add_admins(group, session)))
        buttons.append(self.ui.create_button_view("remove admins",
                                                  lambda s: self.remove_admins(group, session)))
        self.ui.create_button_group_view(session, "What do you want to do?", buttons).draw()

    def change_name(self, group, session):
        self.ui.create_text_view(session, "What is the new group name?").draw()
        self.ui.get_text(session, self.newName)

    def change_description(self, group, session):
        self.ui.create_text_view(session, "What is the new group description?").draw()
        self.ui.get_text(session, self.newDes)

    def add_participants(self, group, session):
        form = AddGroupParticipants(group)
        self.ui.create_form_view(session, form, "Add participants", self.addedP).draw()

    def remove_participants(self, group, session):
        form = RemoveGroupParticipants(group)
        self.ui.create_form_view(session, form, "remove paticipants", self.removeP).draw()

    def remove_admins(self, group, session):
        form = RemoveGroupAdmins(group)
        self.ui.create_form_view(session, form, "Make non-admins", self.removeA).draw()

    def add_admins(self, group, session):
        form = AddGroupAdmins(group)
        self.ui.create_form_view(session, form, "Add admins", self.AddedA).draw()

    def addedP(self, session: Session, form_activity: FormActivity, form: AddGroupAdmins):
        global group2
        users = UserConstraint.get_users_with_constraint(MachzorConstraint(session.user.mahzor))
        new_participants = []
        for u in users:
            if u in group2 or u in form.AddedP.value:
                new_participants.append(u)
        group2.participants = new_participants
        group2.save()
        self.ui.create_text_view(session, "Participants successfully added!").draw()

    def removeP(self, session: Session, form_activity: FormActivity,
                    form: RemoveGroupParticipants):
        global group2
        users = UserConstraint.get_users_with_constraint(MachzorConstraint(session.user.mahzor))
        new_participants = []
        for u in users:
            if u in group2 and u not in form.AddedP.value:
                new_participants.append(u)
        new_admmins = []
        for u in users:
            if u in group2.admins and u not in form.AddedP.value:
                new_admmins.append(u)
            else:
                if len(groups_api.get_user_groups(u)) > 1:
                    t = 0
                    for group in groups_api.get_user_groups(u):
                        if u in group.admins:
                            t = t + 1
                    if t == 1:
                        u.role.remove('admin')
                        u.save()
        group2.participants = new_participants
        group2.admins = new_admmins
        group2.save()
        self.ui.create_text_view(session, "Participants successfully removed!").draw()

    def AddedA(self, session: Session, form_activity: FormActivity, form: AddGroupAdmins):
        global group2
        users = UserConstraint.get_users_with_constraint(MachzorConstraint(session.user.mahzor))
        new_participants = []
        for u in users:
            if u in group2.admins or u in form.AddedA.value:
                new_participants.append(u)
                if 'group_admin' not in u.role:
                    u.role.append('admin')
                    u.save()
        group2.admins = new_participants
        group2.save()
        self.ui.create_text_view(session, "Admins successfully added!").draw()

    def removeA(self, session: Session, form_activity: FormActivity, form: RemoveGroupAdmins):
        global group2
        users = UserConstraint.get_users_with_constraint(MachzorConstraint(session.user.mahzor))
        new_participants = []
        for u in users:
            if u in group2.admins and u not in form.AddedA.value:
                new_participants.append(u)
            else:
                if len(groups_api.get_user_groups(u)) > 1:
                    t = 0
                    for group in groups_api.get_user_groups(u):
                        if u in group.admins:
                            t = t + 1
                    if t == 1:
                        u.role.remove('admin')
                        u.save()
        group2.admins = new_participants
        group2.save()
        self.ui.create_text_view(session, "Admins successfully removed!").draw()

    def newName(self, session, text):
        global group2
        group2.name = text
        group2.save()
        self.ui.create_text_view(session, "Name successfully changed").draw()

    def newDes(self, session, text):
        global group2
        group2.description = text
        group2.save()
        self.ui.create_text_view(session, "Description successfully changed").draw()

    def is_authorized(self, user: User) -> bool:
        return "group_admin" in user.role or "bot_admin" in user.role

    def get_summarize_views(self, session: Session) -> [View]:
        return list()

    def get_command(self) -> str:
        return "vidutz"

    def get_scheduled_jobs(self):
        return list()
