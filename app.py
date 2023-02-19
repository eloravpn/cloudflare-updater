import CloudFlare
import os
import sys
import re
import getopt
from dotenv import load_dotenv
from proxy import load_proxy
import urllib.request

load_dotenv()

# load_proxy()

ip_list = {}


def cli(args):
    """Cloudflare API via command line"""

    usage = ('usage: python app.py '
             + '[-V|--version] [-h|--help] [-p|--printzones] ' +
             '[-u|--url remote-ip-list-url] [-z|--zonename CloudFlare-zone-name]')

    try:
        opts, args = getopt.getopt(args,
                                   'Vhpu:z:',
                                   [
                                       'version',
                                       'help', 'printzones', 'url=', 'zonename='
                                   ])
    except getopt.GetoptError:
        sys.exit(usage)

    for opt, arg in opts:
        if opt in ('-V', '--version'):
            sys.exit('Cloudflare library version: %s' %
                     (CloudFlare.__version__))
        if opt in ('-h', '--help'):
            sys.exit(usage)
        if opt in ('-p', '--printzones'):
            print_zones()
        if opt in ('-u', '--url'):
            read_ip_list(arg)
        if opt in ('-z', '--zonename'):
            print_dns_records(arg)


def read_ip_list(arg):
    print('Start reading ip list from remote: '+arg)

    for line in urllib.request.urlopen(arg):
        ip_full = line.decode('utf-8')
        name = ip_full.split()[0]
        ip = ip_full.split()[1]
        ip_list[name] = ip


def main(args=None):
    """Cloudflare API via command line"""
    if args is None:
        args = sys.argv[1:]
    cli(args)


def print_zones():
    cf = CloudFlare.CloudFlare(
        email=os.environ['EMAIL'], key=os.environ['KEY'])
    zones = cf.zones.get()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print("zone_id=%s zone_name=%s" % (zone_id, zone_name))


def print_dns_records(zone_name):
    print('Zone Name: '+zone_name)
    cf = CloudFlare.CloudFlare(
        email=os.environ['EMAIL'], key=os.environ['KEY'])

    # print the results - first the zone name
    zones = cf.zones.get()
    zone_id = None
    for zone in zones:
        if (zone_name == zone['name']):
            zone_id = zone['id']
            print("Update records in zone id=%s zone_name=%s" %
                  (zone_id, zone_name))

    if (zone_id == None):
        exit('Zone does not found')
    # request the DNS records from that zone
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

    # then all the DNS records for that zone
    for dns_record in dns_records:
        r_zone_id = dns_record['zone_id']
        r_name = dns_record['name']
        r_type = dns_record['type']
        r_content = dns_record['content']
        r_id = dns_record['id']
        r_ttl = dns_record['ttl']

        if (r_name == zone_name):
            continue

        op_name = r_name.split('.')[0].replace('main', '')

        print('Operator: '+op_name.upper())

        try:
            op_ip = ip_list[op_name.upper()]
        except KeyError as e:
            print('Operator Not Found: '+op_name.upper())
            continue

        print('\t IP in remote ip list: '+op_ip)

        print('\t Current DNS Record: ', r_id, r_name, r_type, r_content)

        if op_ip != None and op_ip != '' and op_ip != r_content:
            print('\t DNS Record IP is old!')
            new_dns_record = {
                'zone_id': r_zone_id,
                'id': r_id,
                'type': r_type,
                'name': r_name,
                'content': op_ip,
                'ttl': 1
            }
            new_dns = cf.zones.dns_records.put(
                zone_id, r_id, data=new_dns_record)
            print(new_dns_record)
        else:
            print('\t DNS Record Is Up To Date')


if __name__ == '__main__':
    main()
