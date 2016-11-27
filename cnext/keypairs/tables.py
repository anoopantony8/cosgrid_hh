from django.utils.translation import ugettext_lazy as _
from horizon import tables
from cnext_api import api


class DeleteKeyPairs(tables.BatchAction):
    name = "delete"
    action_present = _("DELETE")
    action_past = _("DELETED")
    data_type_singular = _(" ")
    data_type_plural = _(" ")
    classes = ('btn-danger', 'btn-terminate',)
    success_url = 'horizon:cnext:keypairs:index'
    
    
    def allowed(self, request, datum):
        if "Tenant Admin" in request.session['user_roles']:
            if datum:
                if datum.username != request.user.cnextpublickey:
                    return True
                else:
                    return False
         
        if datum:
            for policy in request.session['user_policies'].get(request.user.cnextname):
                if ("Delete KP" in policy[2] and (datum.provider,datum.region) == (policy[0],policy[1])):
                    if datum.status != request.user.cnextpublickey:
                        return True
        return False

    def action(self, request, obj_id):
        api.delete_keypair(request, obj_id)        


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, key_id):
        #keypair = api.inst_detail(request, key_id)
        return keypairs
 
    def load_cells(self, keypairs=None):
        super(UpdateRow, self).load_cells(keypairs)
        # Tag the row with the image category for client-side filtering.
        #kp = self.datum
        #self.attrs['data-provider'] = kp.provider
        #self.attrs['data-region'] = kp.region   


class ImportKeyPair(tables.LinkAction):
    name = "import"
    verbose_name = _("Import Keypair")
    url = "horizon:cnext:keypairs:import"
    classes = ("ajax-modal", "btn-upload")


class CreateKeyPair(tables.LinkAction):
    name = "create"
    verbose_name = _("Create User")
    url = "horizon:cnext:keypairs:create"
    classes = ("ajax-modal", "btn-create")

    def allowed(self, request, datum):
        for policy in request.session['user_policies'].get(request.user.cnextname):
            if "Create KP" in policy[2]:
                return True
        return False    


class KeypairsTable(tables.DataTable):
    username = tables.Column("username",link=("horizon:cnext:keypairs:detail"), verbose_name=_("UserName"))
    email = tables.Column('email', verbose_name=_("Email"))
    groups = tables.Column('groups', verbose_name=_("Groups"))

    def get_object_id(self, user):
        return user.id

    class Meta:
        name = "users"
        row_class = UpdateRow
        verbose_name = _("Users")
        table_actions = (CreateKeyPair,)
        row_actions = (DeleteKeyPairs,
                       )
