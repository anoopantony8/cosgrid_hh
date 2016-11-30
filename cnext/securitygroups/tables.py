import logging
from django.core.urlresolvers import reverse
from horizon import exceptions, tables
from cnext_api import api
from netjson_api import api as netjson_api
from django.utils.translation import ugettext_lazy as _

LOG = logging.getLogger(__name__)


class DeleteGroup(tables.DeleteAction):
    data_type_singular = _("Security Group")
    data_type_plural = _("Security Groups")
    
    def allowed(self, request, instance):
        if "Tenant Admin" in request.session['user_roles']:
            if instance:
                if instance.status not in ("deleting","deleted",):
                    return True
                else:
                    return False
         
        if instance:
            for policy in request.session['user_policies'].get(request.user.cnextname):
                if ("Delete SG" in policy[2] and (instance.provider.lower(),instance.region.lower()) == (policy[0],policy[1])):
                    if instance.status not in ("deleting","deleted",):
                        return True
        return False
           

    def delete(self, request, obj_id):
        try:
            api. delete_securitygroup(request,obj_id)  
        except Exception:
             
            msg = _('Unable to delete Securitygroup "%s"'
                    'depend on it.')
            exceptions.check_message(["securitygroups", "dependent"], msg % obj_id)
            raise
            
  
class CreateGroup(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Security Group")
    url = "horizon:cnext:securitygroups:create"
    classes = ("ajax-modal", "btn-create")
    
    def allowed(self, request, datum):
        for policy in request.session['user_policies'].get(request.user.cnextname):
            if "Create SG" in policy[2]:
                return True
        return False


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, ca_id):
        ca = netjson_api.ca_view(request, ca_id)
        return ca
 
    def load_cells(self, ca=None):
        super(UpdateRow, self).load_cells(ca)
        # Tag the row with the image category for client-side filtering.
        sg = self.datum
        # self.attrs['data-provider'] = sg.provider
        # self.attrs['data-region'] = sg.region

class AddRule(tables.LinkAction):
    name = "add_rule"
    verbose_name = _("Add Rule")
    url = "horizon:cnext:securitygroups:add_rule"
    classes = ("ajax-modal", "btn-add")
   
    def get_link_url(self, datum):
        return reverse("horizon:cnext:"
                       "securitygroups:add_rule", args=[datum.id])
    def allowed(self, request, instance=None):
        if instance.rules == [] and instance.status not in ("deleted","deleting"):
            return True
        else :
            return False

class AddPort(tables.LinkAction):
    name = "add_port"
    verbose_name = _("Add Port")
    url = "horizon:cnext:securitygroups:add_port"
    classes = ("ajax-modal", "btn-create")
    def get_link_url(self, datum):
        return reverse("horizon:cnext:"
                       "securitygroups:add_port", args=[datum.id])
    
    def allowed(self, request, instance=None):
        if instance.rules != [] and instance.status not in ("deleted","deleting"):
            return True
        else :
            return False 

class DeleteRule(tables.LinkAction):
    name = "delete_rule"
    verbose_name = _("Delete Rule")
    url = "horizon:cnext:securitygroups:delete_rule"
    classes = ("ajax-modal", "btn-deleterule")

    def get_link_url(self, datum):
        return reverse("horizon:cnext:"
                       "securitygroups:delete_rule", args=[datum.id])
    
    def allowed(self, request, instance=None):
        if instance.rules != [] and instance.status not in ("deleted","deleting"):
            return True
        else :
            return False


class SecurityGroupsTable(tables.DataTable):
    name = tables.Column('name', link=("horizon:cnext:securitygroups:detail"), verbose_name=_("Name"))
    notes = tables.Column('notes', verbose_name=_("Notes"))
    digest = tables.Column('digest', verbose_name=_("Digest"))
    organization = tables.Column('organization', verbose_name=_("Organization"))
    validity_end = tables.Column('validity_end', verbose_name=_("Validity End"))

    def get_object_id(self, ca):
        return ca.id

    class Meta:
        name = "securitygroups"
        row_class = UpdateRow
        verbose_name = _("CAs")
        # table_actions = (CreateGroup,)
        # row_actions = (AddRule,DeleteGroup,AddPort,DeleteRule,)

