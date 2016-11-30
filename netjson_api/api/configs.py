import logging
import httplib2
import requests
from cloud_mongo import trail

LOG = logging.getLogger(__name__)


class Config:
    def __init__(self, id, name, backend, status, key, mac_address, templates, vpn, config):
        self.id = id
        self.name = name
        self.backend = backend
        self.status = status
        self.key = key
        self.mac_address = mac_address
        self.templates = templates
        self.vpn = vpn
        self.config = config


def config_list(request):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        configs = list()
        url = endpoint.strip('/') + "/configs/"
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Config List Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            configs_list = body['results']
            for config in configs_list:
                configs.append(Config(config['id'], config['name'], config['backend'], config['status'],
			config['key'], config['mac_address'], config['templates'], config['vpn'], config['config']))
        else:
            raise
        return configs
    except Exception as e:
        logging.debug("Unable to get configs %s" % e.message)
        configs = list()
    return configs

def config_view(request, config_id):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        url = endpoint.strip('/') + "/configs/%s/" % config_id
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Config View Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            return body
        else:
            raise
        return {}
    except Exception as e:
        logging.debug("Unable to get config %s" % e.message)
        return {}

