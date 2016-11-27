
import logging
import httplib2
import requests
from cloud_mongo import trail
from netjson_api.api import groups

LOG = logging.getLogger(__name__)


class User:
    def __init__(self, id, username=None, email=None, groups=None):
        self.id = id
        self.username = username
        self.email = email
        self.groups = groups

def user_create(request, req_body):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        users = list()
        url = endpoint.strip('/') + "/users/"
        resp = requests.post(url=url, auth=(credential_username, credential_password), json=req_body)
        LOG.debug("Users Create Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 201 and body:
            return body
        else:
            raise
        return body
    except Exception as e:
        logging.debug("Unable to create user %s" % e.message)
        return {}

def user_list(request):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        users = list()
        url = endpoint.strip('/') + "/users/"
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Users List Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            users_list = body['results']
            for user in users_list:
                group_names = list()
                for group_url in user['groups']:
                    group_names.append(groups.group_name_from_url(request, group_url))
                group_names = ', '.join(group_names)
                users.append(User(user['id'], user['username'], user['email'], group_names))
        else:
            raise
        return users
    except Exception as e:
        logging.debug("Unable to get users %s" % e.message)
        users = list()
    return users

def user_view(request, user_id):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        url = endpoint.strip('/') + "/users/%s/" % user_id
        resp = requests.get(url=url, auth=(credential_username, credential_password))
        LOG.debug("Users View Status %s" % resp.status_code)
        body = resp.json()
        if resp.status_code == 200 and body:
            group_names = list()
            for group_url in body['groups']:
                group_names.append(groups.group_name_from_url(request, group_url))
            body['groups'] = ', '.join(group_names)
            return body
        else:
            raise
        return {}
    except Exception as e:
        logging.debug("Unable to get user %s" % e.message)
        return {}

def user_delete(request, user_id):
    try:
        credential_username = request.user.cnextpublickey
        credential_password = trail.encode_decode(request.user.cnextprivatekey, "decode")
        endpoint = request.user.cnextendpoint
        httpInst = httplib2.Http()
        httpInst.add_credentials(name=credential_username, password=credential_password)
        users = list()
        url = endpoint.strip('/') + "/users/%s" % user_id
        resp = requests.delete(url=url, auth=(credential_username, credential_password))
        LOG.debug("Users Delete Status %s" % resp.status_code)
        if resp.status_code == 204:
            return True
        else:
            raise
    except Exception as e:
        logging.debug("Unable to create user %s" % e.message)
        return False

