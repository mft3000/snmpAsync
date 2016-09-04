#!/usr/bin/env python      

########## ver 0.1
#
# 0.1 first init
#

import argparse, os, logging
from scapy.all import *

from socket import socket, AF_INET, SOCK_DGRAM

import asyncore

class packet(asyncore.file_dispatcher):

    dst = str()
    comm = str()
    oid = str()

    def __init__(self, dst, comm, oid, debug):
        asyncore.dispatcher.__init__(self)

        self.dst = dst
        self.comm = comm
        self.oid = oid
        self.debug = debug

        self.create_socket(AF_INET, SOCK_DGRAM)
        self.connect((self.dst, 161))

    def handle_read(self):


        r = SNMP( self.recv(4096) )

        if self.debug:
            logging.debug( r.show() )                                                                                                                 
            logging.debug( hexdump(r) )         

        print self.dst, '[', self.comm, ']',
        print r[SNMPvarbind].oid.val, '-', r[SNMPvarbind].value.val

        self.handle_close()

    def writable(self):
        return False

    def handle_connect(self):
        snmp = SNMP(community=self.comm,PDU=SNMPget(varbindlist=[SNMPvarbind(oid=self.oid)]))

        buf = str( snmp )
        while buf:
            bytes = self.send( buf )
            buf = buf[bytes:]

    def handle_close(self):
        self.close()

    def handle_expt(self):
        self.close()


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

    oids = {}
    oids["sysName"] = ".1.3.6.1.2.1.1.5.0"
    oids["sysDescr"] = ".1.3.6.1.2.1.1.1.0"
    oids["cpu-load"] = ".1.3.6.1.2.1.25.3.3.1.2.1"

    for destination in destinations:
        for oid_val in oids.values():
            p = packet( destination, community, oid_val, args.debug)
    
    asyncore.loop()


if __name__ == '__main__':
  main()