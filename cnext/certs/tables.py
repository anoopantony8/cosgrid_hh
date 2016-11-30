import logging
from django.core.urlresolvers import reverse
from horizon import exceptions, tables
from netjson_api import api as netjson_api
from django.utils.translation import ugettext_lazy as _

LOG = logging.getLogger(__name__)


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, cert_id):
        cert = netjson_api.ca_view(request, cert_id)
        return cert
 
    def load_cells(self, cert=None):
        super(UpdateRow, self).load_cells(cert)
        cert = self.datum


class CertsTable(tables.DataTable):
    name = tables.Column('name', link=("horizon:cnext:certs:detail"), verbose_name=_("Name"))
    notes = tables.Column('notes', verbose_name=_("Notes"))
    digest = tables.Column('digest', verbose_name=_("Digest"))
    organization = tables.Column('organization', verbose_name=_("Organization"))
    validity_end = tables.Column('validity_end', verbose_name=_("Validity End"))
    ca = tables.Column('ca', verbose_name=_("CA"))

    def get_object_id(self, cert):
        return cert.id

    class Meta:
        name = "certs"
        row_class = UpdateRow
        verbose_name = _("Certs")

