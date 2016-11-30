from django.utils.translation import ugettext_lazy as _
from horizon import tabs


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("cnext/certs/"
                     "_detail_overview.html")

    def get_context_data(self, request):
        return {"cert": self.tab_group.kwargs['cert']}
    
    

class CertsDetailTabs(tabs.TabGroup):
    slug = "cert_details"
    tabs = (OverviewTab,)
