from django.utils.translation import ugettext_lazy as _

import horizon

from cnext import dashboard


class Snapshots(horizon.Panel):
    name = _("Configs")
    slug = "snapshots"


dashboard.Cnext.register(Snapshots)
