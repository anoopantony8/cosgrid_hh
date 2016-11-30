from django.utils.translation import ugettext_lazy as _
from horizon import tabs


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("cnext/snapshots/"
                     "_detail_overview.html")

    def get_context_data(self, request):
        return {"config": self.tab_group.kwargs['config']}



class ConfigDetailTabs(tabs.TabGroup):
    slug = "instance_details"
    tabs = (OverviewTab,)

