from oauth2_client.credentials_manager import ServiceInformation, CredentialManager
from collections import defaultdict

import json

CLIENT_ID = "secret"
CLIENT_SECRET = "secret"
TOKEN_URL = 'https://cloudsso.cisco.com/as/token.oauth2'
AUTH_URL = 'https://cloudsso.cisco.com/as/authorization.oauth2'

CISCO_BASE = 'https://api.cisco.com'

URI = '/security/advisories/cvrf/product.json?product='

FILTER_KW_MAP = {
    'iosxe': 'ios xe',
    'ios': 'ios',
}

vulnerable = defaultdict(list)


def api_request(client_id, client_secret, uri):
    service_info = ServiceInformation(AUTH_URL,
                                      TOKEN_URL,
                                      client_id,
                                      client_secret,
                                      []
                                      )
    manager = CredentialManager(service_info)
    manager.init_with_client_credentials()

    response = manager.get(CISCO_BASE + uri)
    if response.status_code != 200:
        print("error from server, code = %s, body=\n%s" % (response.status_code, response.text))
        return False
    json_response = json.loads(response.text)
    return json_response['advisories']


def get_device_info(ip, user_name, password) -> dict:
    """get version from device and return tuple: (ip,version)"""
    from .helper import get_version_os
    version, os = get_version_os(ip, user_name, password)
    info = {
        'ip': ip,
        'version': version,
        'os': os
    }
    return info


def scan_device(advisories, device):
    """scan if the device is affected by the collected advisories"""
    global vulnerable
    ip = device['ip']
    version = device['version']
    for advisory in advisories:
        affected_versions = str(advisory['productNames'])
        if version in affected_versions:
            vulnerable[ip].append(advisory['advisoryId'] + "(%s)" % advisory['sir'])


def get_advisories(cisco_os):
    """get the advisories list from API for the given os"""
    filter_ = FILTER_KW_MAP[cisco_os]
    path = URI + filter_
    advisories = api_request(client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET,
                             uri=path
                             )
    return advisories


def run(devices_info: list):
    """
    run the scanner
    :param device_info: {'ip':ip,'version':version, 'os':os}
    :return: affected devices: dict
    """

    scanned = []
    # get advisories from cisco api
    ios_advisories = get_advisories('ios')
    iosxe_adisories = get_advisories('iosxe')

    for device in devices_info:
        if device['os'].lower() == 'ios':
            scan_device(ios_advisories, device)

        elif device['os'].lower() == 'ios-xe':
            scan_device(iosxe_adisories, device)


        else:
            print('unknown OS = ' + device['os'])
            continue
        scanned.append(device['ip'])

    return vulnerable, scanned
