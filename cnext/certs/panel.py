from django.utils.translation import ugettext_lazy as _

import horizon

from cnext import dashboard


class Certs(horizon.Panel):
    name = _("Certs")
    slug = "certs"


dashboard.Cnext.register(Certs)
