#!/usr/bin/env python      

########## ver 0.1
#
# 0.1 first init

from scapy.all import SNMP, SNMPnext, SNMPvarbind, ICMP, SNMPget

from socket import socket, AF_INET, SOCK_DGRAM

import asyncore

class snmp_packet(asyncore.file_dispatcher):

    dst = str()
    comm = str()
    oid = str()

    def __init__(self, dst, comm, oid, debug = False):
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

class snmp_packets(object):

    def __init__(self, dst, comm, oid, debug = False):

        self.dst = dst
        self.comm = comm
        self.oid = oid
        self.debug = debug

        self.snmpwalk()

    def snmpwalk(self):
        
        start_oid = self.oid
        #print start_oid
        print 
        try:
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
                if start_oid not in self.oid:
                    break
                #print oid
                #print '==============='

                
        except KeyboardInterrupt:
            pass

        print '==============='