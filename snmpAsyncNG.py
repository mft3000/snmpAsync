#!/usr/bin/env python      

########## ver 0.1
#
# 0.1 first init
#

import argparse, os, logging, re
from scapy.all import *

from socket import socket, AF_INET, SOCK_DGRAM

import asyncore

def snmpwalk(dst, oid="1", community="public"):
    
    start_oid = oid
    #print start_oid
    print 
    try:
        while 1:
            if start_oid not in oid:
                break

            #print oid
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect((dst, 161))

            snmp = SNMP(community=community,PDU=SNMPnext(varbindlist=[SNMPvarbind(oid=oid)]))

            buf = str( snmp )
            while buf:
                bytes = s.send( buf )
                buf = buf[bytes:]


            r = SNMP( s.recv(4096) )      

            print dst, '[', community, ']',
            print r[SNMPvarbind].oid.val, '-', r[SNMPvarbind].value.val

            if ICMP in r:
                print repr(r)
                break
            if r is None:
                print "No answers"
                break
            #print "%-40s: %r" % (r[SNMPvarbind].oid.val,r[SNMPvarbind].value.val)
            oid = r[SNMPvarbind].oid.val
            #print oid
            #print '==============='

            
    except KeyboardInterrupt:
        pass

    print '==============='

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

    # oids["ospfIfMetricIpAddress"] = "1.3.6.1.2.1.14.8.1.1"
    # oids["ospfIfMetricValue"] = "1.3.6.1.2.1.14.8.1.4"

    # oids["sysName"] = "1.3.6.1.2.1.1.5"

    for destination in destinations:
        for oid_key, oid_val in oids.items():
            print oid_key, oid_val
            snmpwalk(destination, oid_val, community)
    


if __name__ == '__main__':
  main()