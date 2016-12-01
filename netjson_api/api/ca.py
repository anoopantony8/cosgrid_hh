import logging
import httplib2
import requests
from cloud_mongo import trail

LOG = logging.getLogger(__name__)


class Ca:
    def __init__(self, id, name, notes, key_length, digest, validity_start, validity_end,
                  country_code, state, city, organization, email, common_name, extensions,
                  serial_number, certificate, private_key, created, modified):
        self.id = id
        self.name = name
        self.notes = notes
        self.key_length = key_length
        self.digest = digest
        self.validity_start = validity_start
        self.validity_end = validity_end
        self.country_code = country_code
        self.state = state
        self.city = city
        self.organization = organization
        self.email = email
        self.common_name = common_name
        self.extensions = extensions
        self.serial_number = serial_number
        self.certificate = certificate
        self.private_key = private_key
        self.created = created
        self.modified = modified


def ca_list(request):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        cas = list()
        url = endpoint.strip('/') + "/cas/"
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("CA List Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            ca_list = body['results']
            for ca in ca_list:
                cas.append(Ca(
                    ca['id'], ca['name'], ca['notes'], ca['key_length'], ca['digest'], ca['validity_start'],
                    ca['validity_end'],ca['country_code'], ca['state'], ca['city'], ca['organization'], ca['email'],
                    ca['common_name'], ca['extensions'],ca['serial_number'], ca['certificate'], ca['private_key'],
                    ca['created'], ca['modified']))
        else:
            raise
        return cas
    except Exception as e:
        logging.debug("Unable to get cas %s" % e.message)
        cas = list()
    return cas


def ca_view(request, ca_id):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        url = endpoint.strip('/') + "/cas/%s/" % ca_id
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("CA View Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            return body
        else:
            raise
    except Exception as e:
        logging.debug("Unable to get ca %s" % e.message)
        return {}

def ca_name_from_url(request, ca_url):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        resp = requests.get(url=ca_url, auth=(credential_username, credential_password))
        LOG.debug("CA View Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            return body['name']
        else:
            raise
        return ''
    except Exception as e:
        logging.debug("Unable to get CA %s" % e.message)
    return ''
