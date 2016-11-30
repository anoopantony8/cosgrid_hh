import logging
import httplib2
import requests
from cloud_mongo import trail

LOG = logging.getLogger(__name__)


class Template:
    def __init__(self, id, name, backend, template_type, default, auto_cert, config, vpn):
	self.id = id
        self.name = name
        self.backend = backend
        self.template_type = template_type
        self.default = default
        self.auto_cert = auto_cert
        self.vpn = vpn


def template_list(request):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        templates = list()
        url = endpoint.strip('/') + "/templates/"
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Template List Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            templates_list = body['results']
            for template in templates_list:
                templates.append(Template(template['id'], template['name'], template['backend'], template['type'],
					 template['default'], template['auto_cert'], template['config'], template['vpn']))
        else:
            raise
        return templates
    except Exception as e:
        logging.debug("Unable to get templates %s" % e.message)
        templates = list()
    return templates

def template_view(request, template_id):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        url = endpoint.strip('/') + "/templates/%s/" % template_id
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Template View Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            return body
        else:
            raise
        return {}
    except Exception as e:
        logging.debug("Unable to get Template %s" % e.message)
        return {}
