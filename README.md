# ios-iosxe-security-scanner
vulnerabilities scanner for cisco ios and iosxe

to use the script, download `vuln_scanner` command, NOTE: this command compatibile with linux OS only.
for other OS you can run the python script `vuln_scanner.py` (.e.a`python3 vuln_scanner.py [OPTIONS]`)

## example usage

### 1) scan single device:

    advisory_scanner$ python3 vuln_scanner.py --host=192.168.1.10 --username=admin --password=admin
    I0912 00:45:32.719982 139744992458560 vuln_scanner.py:44] scanner started
    I0912 00:45:32.720139 139744992458560 vuln_scanner.py:46] scanning single host 192.168.1.10
    I0912 00:45:33.147540 139744905295616 transport.py:1687] Connected (version 2.0, client Cisco-1.25)
    I0912 00:45:34.427333 139744905295616 transport.py:1687] Authentication (password) successful!
    AFFECTED DEVICES:
    192.168.1.10:
    cisco-sa-20180328-lldp(High)
    cisco-sa-20170629-snmp(High)
    cisco-sa-20170727-ospf(Medium)
    cisco-sa-20170322-dhcpc(High)    
    SCANNED DEVICES:
    ['192.168.1.10']

### 2) scan multiple devices using .conf file:


    advisory_scanner$ python3 vuln_scanner.py --file=devices.conf
    I0912 00:45:32.719982 139744992458560 vuln_scanner.py:44] scanner started
    I0912 00:45:32.720139 139744992458560 vuln_scanner.py:46] scanning hosts in file devices.conf
    I0912 00:45:33.147540 139744905295616 transport.py:1687] Connected (version 2.0, client Cisco-1.25)
    I0912 00:45:34.427333 139744905295616 transport.py:1687] Authentication (password) successful!
    AFFECTED DEVICES:
    192.168.1.10:
    cisco-sa-20180328-lldp(High)
    cisco-sa-20170629-snmp(High)
    cisco-sa-20170727-ospf(Medium)
    cisco-sa-20170322-dhcpc(High)    
    192.168.1.20:
    isco-sa-20130801-lsaospf(Medium)
    SCANNED DEVICES:
    ['192.168.1.10','192.168.1.20']
    
`devices.conf` file:

    # ip,username,password
    192.168.1.10,admin,admin
    192.168.1.20,admin,admin
    
