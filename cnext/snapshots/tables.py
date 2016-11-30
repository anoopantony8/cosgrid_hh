from django.utils.translation import ugettext_lazy as _
from horizon import tables
from netjson_api import api as netjson_api


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, snap_id):
        #configs = netjson_api(request, snap_id)
        return configs
 
    def load_cells(self, configs=None):
        super(UpdateRow, self).load_cells(configs)
        # Tag the row with the image category for client-side filtering.
        #snap_shots = self.datum
        #self.attrs['data-provider'] = snap_shots.provider
        #self.attrs['data-region'] = snap_shots.region     


class SnapshotTable(tables.DataTable):
    name = tables.Column("name", link=("horizon:cnext:snapshots:detail"), verbose_name=_("Name"))
    status = tables.Column("status", verbose_name=_("Status"))
    backend = tables.Column("backend", verbose_name=_("Backend"))
    key = tables.Column("key", verbose_name=_("Key"))
    mac_address = tables.Column("mac_address", verbose_name=_("MAC Address"))
    templates = tables.Column("templates", verbose_name=_("Templates"))
    vpn = tables.Column("vpn", verbose_name=_("VPN"))

    def get_object_id(self, config):
        return config.id
    
    class Meta:
        name = "snapshots"
        row_class = UpdateRow
        verbose_name = _("Configs")
