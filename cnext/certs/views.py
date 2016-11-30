
import logging
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions, forms,tabs, tables
from cnext.certs import tabs as project_tabs
from .tables import CertsTable
from netjson_api import api as netjson_api

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = CertsTable
    template_name = 'cnext/certs/index.html'

    def get_data(self):
        try:
            certs = netjson_api.cert_list(self.request)
        except:
            certs = []
            exceptions.handle(self.request,
                              _('Unable to retrieve certs'))
        return certs
     
    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        return context

class DetailView(tabs.TabView):
    tab_group_class = project_tabs.CertsDetailTabs
    template_name = 'cnext/certs/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["certs"] = self.get_data()
        return context
    
    def get_data(self):
            try:
                cert = netjson_api.cert_view(self.request, self.kwargs['cert_id'])
                return cert
            except Exception:
                redirect = reverse('horizon:cnext:certs:index')
                exceptions.handle(self.request,
                                  _('Unable to retrieve Cert details.'),
                                  redirect=redirect)

    def get_tabs(self, request, *args, **kwargs):
        cert = self.get_data()
        return self.tab_group_class(request, cert=cert, **kwargs)
