from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from horizon import messages,tables
from hpcloud import api

ENABLE = 0
DISABLE = 1


class CreateUserLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create User")
    url = "horizon:hpcloud:users:create"
    classes = ("ajax-modal", "btn-create")
    policy_rules = (('identity', 'identity:create_grant'),
                    ("identity", "identity:create_user"),
                    ("identity", "identity:list_roles"),
                    ("identity", "identity:list_projects"),)

    def allowed(self, request, user):
        return api.keystone.keystone_can_edit_user()


class EditUserLink(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:hpcloud:users:update"
    classes = ("ajax-modal", "btn-edit")
    policy_rules = (("identity", "identity:update_user"),
                    ("identity", "identity:list_projects"),)

    def get_policy_target(self, request, user):
        return {"user_id": user.id}

    def allowed(self, request, user):
        return api.keystone.keystone_can_edit_user()


class ToggleEnabled(tables.BatchAction):
    name = "toggle"
    action_present = (_("Enable"), _("Disable"))
    action_past = (_("Enabled"), _("Disabled"))
    data_type_singular = _("User")
    data_type_plural = _("Users")
    classes = ("btn-toggle",)
    policy_rules = (("identity", "identity:update_user"),)

    def get_policy_target(self, request, user=None):
        if user:
            return {"user_id": user.id}
        return {}

    def allowed(self, request, user=None):
        if not api.keystone.keystone_can_edit_user():
            return False

        self.enabled = True
        if not user:
            return self.enabled
        self.enabled = user.enabled
        if self.enabled:
            self.current_present_action = DISABLE
        else:
            self.current_present_action = ENABLE
        return True

    def update(self, request, user=None):
        super(ToggleEnabled, self).update(request, user)
        if user and user.id == request.user.id:
            self.attrs["disabled"] = "disabled"

    def action(self, request, obj_id):
        if obj_id == request.user.id:
            messages.info(request, _('You cannot disable the user you are '
                                     'currently logged in as.'))
            return
        if self.enabled:
            api.keystone.user_update_enabled(request, obj_id, False)
            self.current_past_action = DISABLE
        else:
            api.keystone.user_update_enabled(request, obj_id, True)
            self.current_past_action = ENABLE


class DeleteUsersAction(tables.DeleteAction):
    data_type_singular = _("User")
    data_type_plural = _("Users")
    policy_rules = (("identity", "identity:delete_user"),)

    def allowed(self, request, datum):
        if not api.keystone.keystone_can_edit_user() or \
                (datum and datum.id == request.user.id):
            return False
        return True

    def delete(self, request, obj_id):
        api.keystone.user_delete(request, obj_id)


class UserFilterAction(tables.FilterAction):
    def filter(self, table, users, filter_string):
        """ Naive case-insensitive search """
        q = filter_string.lower()
        return [user for user in users
                if q in user.name.lower()
                or q in user.email.lower()]


class UsersTable(tables.DataTable):
    STATUS_CHOICES = (
        ("true", True),
        ("false", False)
    )
    name = tables.Column('name', verbose_name=_('User Name'))
    email = tables.Column('email', verbose_name=_('Email'),
                          filters=[defaultfilters.urlize])
    id = tables.Column('id', verbose_name=_('User ID'))
    enabled = tables.Column('enabled', verbose_name=_('Enabled'),
                            status=True,
                            status_choices=STATUS_CHOICES,
                            empty_value="False")

    class Meta:
        name = "users"
        verbose_name = _("Users")
        row_actions = (EditUserLink, ToggleEnabled, DeleteUsersAction)
        table_actions = (UserFilterAction, CreateUserLink, DeleteUsersAction)
