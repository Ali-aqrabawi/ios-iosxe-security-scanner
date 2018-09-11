from netmiko import NetMikoAuthenticationException, NetmikoAuthError, NetmikoTimeoutError, NetMikoTimeoutException

from netmiko import ConnectHandler
import re

def create_connection(device):
    device['device_type'] = 'cisco_xe'
    try:
        connection = ConnectHandler(**device)
    except (NetMikoTimeoutException, NetmikoTimeoutError):
        print("error: connection timeout to device = " + device['ip'])
        return False
    except (NetmikoAuthError, NetMikoAuthenticationException):
        print("error: auth failed to device = " + device['ip'])
        return False
    return connection


def extract_version(output: str):
    regex = r'Version\s+(.*),'
    match = re.search(regex, output)
    if not match:
        return False
    return match.group(1)

def extract_os(output: str):
    regex = r'Cisco\s+(.*)\s+Software,'
    match = re.search(regex, output)
    if not match:
        return False
    return match.group(1)

def get_version_os(ip,user_name,password):
    device = {
        'ip':ip,
        'username':user_name,
        'password':password
    }
    conn = create_connection(device)
    if not conn:
        return False
    show_version = conn.send_command("show version")
    version = extract_version(show_version)
    os = extract_os(show_version)
    return version,os

