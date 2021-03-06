'''
Created on 28-Mar-2014

@author: annamalai
'''
from django.utils.translation import ugettext_lazy as _
from horizon import tabs

class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("amazon/instances/"
                     "_detail_overview.html")

    def get_context_data(self, request):
        return {"instance": self.tab_group.kwargs['instance']}


class InstanceDetailTabs(tabs.TabGroup):
    slug = "instance_details"
    tabs = (OverviewTab,)