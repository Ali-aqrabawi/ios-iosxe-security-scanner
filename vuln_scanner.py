from csa_scanner.scanner import run, get_device_info
from termcolor import cprint
from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS

flags.DEFINE_string('file',
                    'devices.conf',
                    'filename/path of the devices.conf file')

flags.DEFINE_string('host',
                    '',
                    'enter single host to scan')

flags.DEFINE_string('username',
                    'admin',
                    'device username')

flags.DEFINE_string('password',
                    'admin',
                    'device password')


def read_from_file(file):
    """read hosts from file"""
    all_devices = []
    with open(file,'r') as f:
        for line in f:
            if '#' in line:
                continue
            ip,username,password = line.split(',')
            device = {
                'ip':ip.strip(),
                'user_name':username.strip(),
                'password':password.strip()
            }
            all_devices.append(device)
    return all_devices


def main(argv):
    logging.info('scanner started')
    if FLAGS.host:
        logging.info(f"scanning single host {FLAGS.host}")
        devices_info = [
            get_device_info(ip=FLAGS.host, user_name=FLAGS.username, password=FLAGS.password)]  # scan take list-like
    else:
        logging.info(f"scanning hosts in file {FLAGS.file}")
        devices = read_from_file(FLAGS.file)
        devices_info = [get_device_info(**dev) for dev in devices]


    affected_hosts, scanned_hosts = run(devices_info=devices_info)

    # printing results
    cprint("AFFECTED DEVICES:", color='yellow')
    for host,advisories in dict(affected_hosts).items():
        cprint(host + ':',color='red')
        for advisory in advisories:
            print(advisory)

    cprint("SCANNED DEVICES:",color='green')
    print(scanned_hosts)


if __name__ == '__main__':
    app.run(main)
