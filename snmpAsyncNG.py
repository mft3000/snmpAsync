#!/usr/bin/env python      

########## ver 0.2
#
# 0.1 first init
# 0.2 add async - PARTIAL
#

import argparse, os, logging, re
from scapy.all import *

from socket import socket, AF_INET, SOCK_DGRAM

import asyncore

class packet(asyncore.file_dispatcher):

    dst = str()
    comm = str()
    oid = str()

    response = str()

    def __init__(self, dst, comm, oid, debug = False):
        asyncore.dispatcher.__init__(self)

        self.dst = dst
        self.comm = comm
        self.oid = oid
        self.debug = debug

        self.snmpwalk()

    def handle_read(self):
        pass

    def writable(self):
        return False

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_expt(self):
        self.close()

    def snmpwalk(self):
        
        start_oid = self.oid
        #print start_oid
        print 
        try:
            while 1:
                if start_oid not in self.oid:
                    break

                #print oid
                s = socket(AF_INET, SOCK_DGRAM)
                s.connect((self.dst, 161))

                snmp = SNMP(community=self.comm,PDU=SNMPnext(varbindlist=[SNMPvarbind(oid=self.oid)]))

                buf = str( snmp )
                while buf:
                    bytes = s.send( buf )
                    buf = buf[bytes:]

                response = SNMP( s.recv(4096) )

                print self.dst, '[', self.comm, ']',
                print response[SNMPvarbind].oid.val, '-', response[SNMPvarbind].value.val

                if ICMP in response:
                    print repr(response)
                    break
                if response is None:
                    print "No answers"
                    break
                #print "%-40s: %r" % (r[SNMPvarbind].oid.val,r[SNMPvarbind].value.val)
                self.oid = response[SNMPvarbind].oid.val
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

    oids["ospfIfMetricIpAddress"] = "1.3.6.1.2.1.14.8.1.1"
    oids["ospfIfMetricValue"] = "1.3.6.1.2.1.14.8.1.4"

    oids["sysName"] = "1.3.6.1.2.1.1.5"

    for destination in destinations:
        for oid_key, oid_val in oids.items():
            print oid_key, oid_val
            # snmpwalk(destination, oid_val, community)
            p = packet( destination, community, oid_val )

    asyncore.loop()


if __name__ == '__main__':
  main()