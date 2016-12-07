#!/usr/bin/env python      

########## ver 0.32
#
# 0.1 first init
# 0.2 add async - PARTIAL
# 0.3 asyncore for snmpGET and snmpwalk for snmpNEXT
# 0.31 create obj for walk
# 0.32 mv objs to lib
#

import argparse, os, logging, re

from libSnmp import snmp_packets, snmp_packet

import asyncore

def main():

    #load_mib("mib/*")

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-r','--router', required=True, nargs='+')
    parser.add_argument('-c','--community', required=False, default='')
    parser.add_argument('-d','--debug', required=False, action='store_true')

    args = parser.parse_args()

    # ++++++++++++++++++++  
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # --------------------  

    destinations = args.router

    community = os.environ['COMMUNITY'] if args.community == '' else args.community

    print "community:", community
    print

    oids = {}
    oids["ifIndex"] = "1.3.6.1.2.1.2.2.1.1"
    oids["ifDescr"] = "1.3.6.1.2.1.2.2.1.2"
    
    oids["ipAdEntAddr"] = "1.3.6.1.2.1.4.20.1.1"
    oids["ipAdEntIfIndex"] = "1.3.6.1.2.1.4.20.1.2"
    oids["ipAdEntNetMask"] = "1.3.6.1.2.1.4.20.1.3"

    oids["ospfIfMetricIpAddress"] = "1.3.6.1.2.1.14.8.1.1"
    oids["ospfIfMetricValue"] = "1.3.6.1.2.1.14.8.1.4"

    for destination in destinations:
        for oid_key, oid_val in oids.items():
            print oid_key, oid_val
            ps = snmp_packets(destination, community, oid_val)

    oids = {}
    oids["sysName"] = "1.3.6.1.2.1.1.5.0"
    oids["sysDescr"] = "1.3.6.1.2.1.1.1.0"
    oids["sysObjectID"] = "1.3.6.1.2.1.1.2.0"

    for destination in destinations:
        for oid_key, oid_val in oids.items():
            print oid_key, oid_val
            p = snmp_packet( destination, community, oid_val, args.debug)
    
    asyncore.loop()


if __name__ == '__main__':
  main()