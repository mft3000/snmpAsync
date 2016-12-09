#!/usr/bin/env python

########## ver 0.3
#
# 0.1 first init
# 0.2 perform oid translation
# 0.21 add scapy mib translation, fix logging debug packet
# 0.3 translate sysObjectID to name, add info to table
#

from scapy.all import SNMP, SNMPnext, SNMPvarbind, ICMP, SNMPget, load_mib, hexdump

from socket import socket, AF_INET, SOCK_DGRAM

import asyncore

from libTable import table

# ++++++++++++++++++++  
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------  

load_mib("mib/*")

class snmp_packet(asyncore.file_dispatcher):

    dst = str()
    comm = str()
    oid = str()

    def __init__(self, dst, comm, oid_key, oid_val, debug = False, translate = True):
        asyncore.dispatcher.__init__(self)

        self.dst = dst
        self.comm = comm
        self.oid = oid_val
        self.oid_key = oid_key
        self.debug = debug
        self.translate = translate

        self.create_socket(AF_INET, SOCK_DGRAM)
        self.connect((self.dst, 161))

    def handle_read(self):

        response = SNMP( self.recv(4096) )

        if self.debug:
            logging.debug( response.show() )                                                                                                                 
            logging.debug( hexdump(response) )

        print self.dst, '[', self.comm, ']',
        if self.translate:
            # print response[SNMPvarbind].oid.val.replace(self.oid, self.oid_key), 
            print response[SNMPvarbind].oid.__oidname__(),
        else:
            print response[SNMPvarbind].oid.val,

        if 'sysObjectID' not in self.oid_key:
            print '-', response[SNMPvarbind].value.val
        else:
            print '-', response[SNMPvarbind].value.__oidname__()


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

class snmp_packets(object):

    def __init__(self, dst, comm, oid_key, oid_val, debug = False, translate = True):

        self.dst = dst
        self.comm = comm
        self.oid = oid_val
        self.oid_key = oid_key
        self.debug = debug
        self.translate = translate

        self.snmpwalk()

    def snmpwalk(self):
        
        start_oid = self.oid
        #print start_oid
        print 
        try:
            t = table(self.oid_key)
            while 1:

                #print oid
                s = socket(AF_INET, SOCK_DGRAM)
                s.connect((self.dst, 161))

                snmp = SNMP(community=self.comm,PDU=SNMPnext(varbindlist=[SNMPvarbind(oid=self.oid)]))

                buf = str( snmp )
                while buf:
                    bytes = s.send( buf )
                    buf = buf[bytes:]

                response = SNMP( s.recv(4096) )

                if self.debug:
                    logging.debug( response.show() )                                                                                                                 
                    logging.debug( hexdump(response) )  

                self.oid = response[SNMPvarbind].oid.val
                if start_oid not in self.oid:
                    break

                print self.dst, '[', self.comm, ']',
                if self.translate:
                    # print response[SNMPvarbind].oid.val.replace(start_oid, self.oid_key), 
                    print response[SNMPvarbind].oid.__oidname__(),
                else:
                    print response[SNMPvarbind].oid.val, 
                print '-', response[SNMPvarbind].value.val

                field = response[SNMPvarbind].oid.__oidname__()
                v = t.add_fields_name(field)
                k = t.add_keys_name(field)
                t.add_values(k, v, response[SNMPvarbind].value.val)

                if ICMP in response:
                    print repr(response)
                    break
                if response is None:
                    print "No answers"
                    break
                #print "%-40s: %r" % (r[SNMPvarbind].oid.val,r[SNMPvarbind].value.val)
                #print oid
                #print '==============='

                
        except KeyboardInterrupt:
            pass

        # print t.show_fileds_list()
        # print t.show_keys_list()
        # print t.show_values_json()
        t.print_table()
        print '==============='