
import logging
import httplib2
import requests
from cloud_mongo import trail

LOG = logging.getLogger(__name__)


class Group:
    def __init__(self, id, url=None, name=None):
        self.id = id
        self.url = url
        self.name = name


def group_list(request):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        groups = list()
        url = endpoint.strip('/') + "/groups/"
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Groups List Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            group_list = body['results']
            for group in group_list:
                groups.append(Group(group['id'], group['url'], group['name']))
        else:
            raise
        return groups
    except Exception as e:
        logging.debug("Unable to get groups %s" % e.message)
        groups = list()
    return groups

def group_view(request, group_id):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        url = endpoint.strip('/') + "/groups/%s/" % user_id
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Group View Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            return body
        else:
            raise
        return {}
    except Exception as e:
        logging.debug("Unable to get group %s" % e.message)
        return {}

def group_name_from_url(request, group_url):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        resp = requests.get(url=group_url, auth=(credential_username, credential_password))
        LOG.debug("Group View Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            return body['name']
        else:
            raise
        return ''
    except Exception as e:
        logging.debug("Unable to get group %s" % e.message)
    return ''

