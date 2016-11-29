from django.utils.translation import ugettext_lazy as _

import horizon

from cnext import dashboard


class Volume(horizon.Panel):
    name = _("Templates")
    slug = "volume"


dashboard.Cnext.register(Volume)
