#!/usr/bin/env python

########## ver 0.42
#
# 0.1 first init
# 0.2 perform oid translation
# 0.21 add scapy mib translation, fix logging debug packet
# 0.3 translate sysObjectID to name, add info to table
# 0.4 print sql table (list, json, textable)
# 0.41 add comments
# 0.42 adjust sql tablet reset
#

from scapy.all import SNMP, SNMPnext, SNMPvarbind, ICMP, SNMPget, load_mib, hexdump

from socket import socket, AF_INET, SOCK_DGRAM

import asyncore, binascii

from libTable import table

def convertMac(octet):
    """
    This Function converts a binary mac address to a hexadecimal string representation
    """
    mac = [binascii.b2a_hex(x) for x in list(octet)]
    return ":".join(mac)
 
def convertIP(octet):
    ip = [str(int(binascii.b2a_hex(x),16)) for x in list(octet)]
    return ".".join(ip)

def normalize_snmp_result(snmp_field, snmp_value):

    if not snmp_field:
        return ''
    elif 'ifPhysAddress' in snmp_field:
        return convertMac(snmp_value)
    else:
        return snmp_value

# ++++++++++++++++++++  
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------  

load_mib("mib/*")

class snmp_packet(asyncore.file_dispatcher):
    '''
    snmpGET query
    '''

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
    '''
    snmpNEXT query
    '''

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
                print '-', 
                # print type(response[SNMPvarbind].value.val),

                field = response[SNMPvarbind].oid.__oidname__()

                #31.223.255.13 [ NordEx7 ] ospfAreaStatus.0.0.0.0 - 1
                #                          ^^^^^^^^^^^^^^ ^^^^^^^   ^
                #                                v           k     res

                v = t.add_fields_name(field)
                k = t.add_keys_name(field)
                res = normalize_snmp_result(v, response[SNMPvarbind].value.val)
                t.add_values(k, v, res)

                print res

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

        # print t.show_fields_list()

        # ['ospfSpfRuns', 'ospfAsBdrRtrCount', 'ospfAreaId', 'ospfAreaLsaCount', 'ospfAuthType', 'ospfAreaStatus', 'ospfAreaLsaCksumSum', 'ospfImportAsExtern', 'ospfAreaSummary', 'ospfAreaBdrRtrCount']
        
        # print t.show_keys_list()

        # ['0.0.0.0']

        print t.show_values_json()

        # {
        #     "0.0.0.0": {
        #         "ospfAreaBdrRtrCount": 2,
        #         "ospfAreaId": "0.0.0.0",
        #         "ospfAreaLsaCksumSum": 13869839,
        #         "ospfAreaLsaCount": 437,
        #         "ospfAreaStatus": 1,
        #         "ospfAreaSummary": 2,
        #         "ospfAsBdrRtrCount": 1,
        #         "ospfAuthType": 0,
        #         "ospfImportAsExtern": 1,
        #         "ospfSpfRuns": 30842
        #     }
        # }

        t.populate_sql_table()

        # INFO:root:loading row to sql...DONE
 
        # t.print_sql_table('list')

        # [ ('ospfSpfRuns', 'ospfAsBdrRtrCount', 'ospfAreaId', 'ospfAreaLsaCount', '-', 'ospfAuthType', 'ospfAreaStatus', 'ospfAreaLsaCksumSum', 'ospfImportAsExtern', 'ospfAreaSummary', 'ospfAreaBdrRtrCount'), 
        # (u'30842', u'1', u'0.0.0.0', u'437', u'0.0.0.0', u'0', u'1', u'13869839', u'1', u'2', u'2') ]

        t.print_sql_table('texttable')

        # +------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
        # | ospfSpfRun | ospfAsBdrR | ospfAreaId | ospfAreaLs |     -      | ospfAuthTy | ospfAreaSt | ospfAreaLs | ospfImport | ospfAreaSu | ospfAreaBd |
        # |     s      |  trCount   |            |   aCount   |            |     pe     |    atus    | aCksumSum  |  AsExtern  |   mmary    | rRtrCount  |
        # +============+============+============+============+============+============+============+============+============+============+============+
        # | 30842      | 1          | 0.0.0.0    | 437        | 0.0.0.0    | 0          | 1          | 13869839   | 1          | 2          | 2          |
        # +------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
        
        # t.print_sql_table('json')

        # [
        #     {
        #         "0.0.0.0": {
        #             "ospfAreaBdrRtrCount": "2",
        #             "ospfAreaId": "0.0.0.0",
        #             "ospfAreaLsaCksumSum": "13869839",
        #             "ospfAreaLsaCount": "437",
        #             "ospfAreaStatus": "1",
        #             "ospfAreaSummary": "2",
        #             "ospfAsBdrRtrCount": "1",
        #             "ospfAuthType": "0",
        #             "ospfImportAsExtern": "1",
        #             "ospfSpfRuns": "30842"
        #         }
        #     }
        # ]

        print '==============='
