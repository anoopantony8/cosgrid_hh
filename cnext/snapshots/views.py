from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions, forms, tables, tabs
from .tables import SnapshotTable
from cnext.snapshots \
    import forms as project_forms
from cnext.snapshots import tabs as project_tabs
from cnext_api import api
from netjson_api import api as netjson_api

class IndexView(tables.DataTableView):
    # A very simple class-based view...
    template_name = 'cnext/snapshots/index.html'
    table_class = SnapshotTable

    def get_data(self):
        try:
            configs = netjson_api.config_list(self.request)
        except:
            configs = []
            exceptions.handle(self.request,_('Unable to retrieve configs.'))
        return configs
    def get_context_data(self,**kwargs):
        context = super(IndexView, self).get_context_data()
        #context["provider"] = api.providers(self.request)
        #context["region"] = api.region(self.request)
        return context

class DetailView(tabs.TabView):
    tab_group_class = project_tabs.ConfigDetailTabs
    template_name = 'cnext/snapshots/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["configs"] = self.get_data()
        return context

    def get_data(self):
            try:
                config = netjson_api.config_view(self.request, self.kwargs['config_id'])
            except Exception, e:
                redirect = reverse('horizon:cnext:snapshots:index')
                exceptions.handle(self.request,
                                  _('Unable to retrieve config details.'),
                                  redirect=redirect)
            return config

    def get_tabs(self, request, *args, **kwargs):
        config = self.get_data()
        return self.tab_group_class(request, config=config, **kwargs)    
    
class CreateView(forms.ModalFormView):
    form_class = project_forms.CreateSnapshot
    template_name = 'cnext/snapshots/create.html'
    success_url = reverse_lazy("horizon:cnext:snapshots:index")



    def get_initial(self):
        return {"instance_name": self.kwargs["instance_name"],"instance_id": self.kwargs["instance_id"],"provider": self.kwargs["provider"],"region": self.kwargs["region"]}
    

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['instance_id'] = self.kwargs["instance_id"]
        context['provider'] = self.kwargs["provider"]
        context['region'] = self.kwargs["region"]
        context['instance_name'] = self.kwargs["instance_name"]
        return context
