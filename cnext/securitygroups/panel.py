from django.utils.translation import ugettext_lazy as _

import horizon

from cnext import dashboard


class Securitygroups(horizon.Panel):
    name = _("CAs")
    slug = "securitygroups"


dashboard.Cnext.register(Securitygroups)
