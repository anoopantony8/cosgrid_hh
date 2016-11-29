import logging
import httplib2
import requests
from cloud_mongo import trail

LOG = logging.getLogger(__name__)


class VPN:
    def __init__(self, name, host, backend, ca, cert, notes=None):
        self.name = name,
        self.host = host,
        self.backend = backend,
        self.ca = ca,
        self.cert = cert,
        self.notes = notes


def vpn_list(request):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        vpns = list()
        url = endpoint.strip('/') + "/vpns/"
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("VPN List Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            vpns_list = body['results']
            for vpn in vpns_list:
                vpns.append(VPN(vpn['name'], vpn['host'], vpn['backend'],
					 vpn['ca'], vpn['cert'], vpn['notes']))
        else:
            raise
        return vpns
    except Exception as e:
        logging.debug("Unable to get vpns %s" % e.message)
        vpns = list()
    return vpns

