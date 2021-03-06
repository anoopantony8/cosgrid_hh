
import logging
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions, forms,tabs, tables
from cnext.securitygroups import forms as project_forms
from cnext.securitygroups import tabs as project_tabs
from .tables import SecurityGroupsTable
from cnext_api import api
from netjson_api import api as netjson_api

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = SecurityGroupsTable
    template_name = 'cnext/securitygroups/index.html'

    def get_data(self):
        try:
            cas = netjson_api.ca_list(self.request)
        except:
            cas = []
            exceptions.handle(self.request,
                              _('Unable to retrieve cas'))
        return cas
     
    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        # context["provider"] = api.providers(self.request)
        # context["region"] = api.region(self.request)
        return context


class AddRuleView(forms.ModalFormView):
    
    form_class = project_forms.AddRule
    template_name = 'cnext/securitygroups/add_rule.html'
    success_url = reverse_lazy("horizon:cnext:securitygroups:index")
    def get_context_data(self, **kwargs):
        context = super(AddRuleView, self).get_context_data(**kwargs)
        context['security_group_id'] = self.kwargs["security_group_id"]
        return context

    def get_initial(self):
        inst_id = self.kwargs["security_group_id"]
        return {'instanceid':inst_id}

class DeleteRuleView(forms.ModalFormView):
    
    form_class = project_forms.DeleteRule
    template_name = 'cnext/securitygroups/delete_rule.html'
    success_url = reverse_lazy("horizon:cnext:securitygroups:index")
    def get_context_data(self, **kwargs):
        context = super(DeleteRuleView, self).get_context_data(**kwargs)
        context['security_group_id'] = self.kwargs["security_group_id"]
        return context

    def get_initial(self):
        inst_id = self.kwargs["security_group_id"]
        sg_rules = api.get_rules(request=self.request,sg_id=inst_id)
        rulelist = []
        for i in range(0,len(sg_rules)):
            rulelist.append((i,("Rule: %s , %s , %s , %s" % (sg_rules[i].from_port,sg_rules[i].to_port,sg_rules[i].protocol,sg_rules[i].cidr_ip))))
        return {'instanceid':inst_id,
                'rule_list':rulelist }


class CreateView(forms.ModalFormView):
    form_class = project_forms.CreateGroup
    template_name = 'cnext/securitygroups/create.html'
    success_url = reverse_lazy('horizon:cnext:securitygroups:index')


class AddPortView(forms.ModalFormView):
    form_class = project_forms.AddPort
    template_name = 'cnext/securitygroups/add_port.html'
    success_url = reverse_lazy("horizon:cnext:securitygroups:index")
    def get_context_data(self, **kwargs):
        context = super(AddPortView, self).get_context_data(**kwargs)
        context['security_group_id'] = self.kwargs["security_group_id"]
        return context

    def get_initial(self):
        inst_id = self.kwargs["security_group_id"]
        return {'instanceid':inst_id}
    

class DetailView(tabs.TabView):
    tab_group_class = project_tabs.SecuritygroupsDetailTabs
    template_name = 'cnext/securitygroups/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["cas"] = self.get_data()
        return context
    
    def get_data(self):
            try:
                ca = netjson_api.ca_view(self.request, self.kwargs['ca_id'])
                return ca
            except Exception:
                redirect = reverse('horizon:cnext:securitygroups:index')
                exceptions.handle(self.request,
                                  _('Unable to retrieve ca details.'),
                                  redirect=redirect)

    def get_tabs(self, request, *args, **kwargs):
        ca = self.get_data()
        return self.tab_group_class(request, ca=ca, **kwargs)
