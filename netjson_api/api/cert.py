import logging
import httplib2
import requests
from cloud_mongo import trail

LOG = logging.getLogger(__name__)


class Cert:
    def __init__(self, id, name, notes, key_length, digest, validity_start, validity_end,
                  country_code, state, city, organization, email, common_name, extensions,
                  serial_number, certificate, private_key, created, modified, revoked, revoked_at, ca):
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
        self.revoked = revoked
        self.revoked_at = revoked_at
        self.ca = ca


def cert_list(request):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        certs = list()
        url = endpoint.strip('/') + "/certs/"
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Cert List Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            ca_list = body['results']
            for cert in ca_list:
                certs.append(Cert(
                    cert['id'], cert['name'], cert['notes'], cert['key_length'], cert['digest'], cert['validity_start'],
                    cert['validity_end'],cert['country_code'], cert['state'], cert['city'], cert['organization'], cert['email'],
                    cert['common_name'], cert['extensions'],cert['serial_number'], cert['certificate'], cert['private_key'],
                    cert['created'], cert['modified'], cert['revoked'], cert['revoked_at'], cert['ca']))
        else:
            raise
        return certs
    except Exception as e:
        logging.debug("Unable to get certs %s" % e.message)
        certs = list()
    return certs


def cert_view(request, cert_id):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        url = endpoint.strip('/') + "/certs/%s/" % cert_id
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Cert View Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            return body
        else:
            raise
    except Exception as e:
        logging.debug("Unable to get cert %s" % e.message)
        return {}

