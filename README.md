SNMP polling with Scapy and Async
=====

perform snmpGet (with Async) and snmpWalk, with scapy.

snmp results will be turned in json format -> sql -> list / texttable / json (for further handle)

oid translation will be perforformed if needed

```
$ python snmpAsyncNG.py -h
WARNING: No route found for IPv6 destination :: (no default route?)
usage: snmpAsyncNG.py [-h] -r ROUTER [ROUTER ...] [-c COMMUNITY] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -r ROUTER [ROUTER ...], --router ROUTER [ROUTER ...]
  -c COMMUNITY, --community COMMUNITY
  -d, --debug
```

NEXT STEPS:
- table join -> json
- help ![igpDraw](https://github.com/mft3000/igpDraw.git) to retrieve ospf data for graph


snmp and Async
===

snmpGET w or w/o Async from ```tcpdump port snmp``` point of view:

- snmpGet w/o Async

```
20:35:39.150716 IP 10.64.0.9.65081 > 10.64.0.250.snmp:  GetRequest(25)  system.sysName.0
20:35:39.152709 IP 10.64.0.250.snmp > 10.64.0.9.65081:  GetResponse(44)  system.sysName.0="SW-Nuovo"
20:35:39.153448 IP 10.64.0.9.60076 > 10.64.0.250.snmp:  GetRequest(25)  system.sysObjectID.0
20:35:39.155574 IP 10.64.0.250.snmp > 10.64.0.9.60076:  GetResponse(34)  system.sysObjectID.0=E:cisco.1.563
20:35:39.157933 IP 10.64.0.9.57603 > 10.64.0.250.snmp:  GetRequest(25)  system.sysDescr.0
20:35:39.155574 IP 10.64.0.250.snmp > 10.64.0.9.57603:  GetResponse(280)  system.sysDescr.0=43_69_73_63_6f_20_49_4f_53_20_53_6f_66_74_77_61_72_65_2c_20_43_33_35_36_30_20_53_6f_66_74_77_61_72_65_20_28_43_33_35_36_30_2d_49_50_53_45_52_56_49_43_45_53_4b_39_2d_4d_29_2c_20_56_65_72_73_69_6f_6e_20_31_32_2e_32_28_35_33_29_53_45_32_2c_20_52_45_4c_45_41_53_45_20_53_4f_46_54_57_41_52_45_20_28_66_63_33_29_0d_0a_54_65_63_68_6e_69_63_61_6c_20_53_75_70_70_6f_72_74_3a_20_68_74_74_70_3a_2f_2f_77_77_77_2e_63_69_73_63_6f_2e_63_6f_6d_2f_74_65_63_68_73_75_70_70_6f_72_74_0d_0a_43_6f_70_79_72_69_67_68_74_20_28_63_29_20_31_39_38_36_2d_32_30_31_30_20_62_79_20_43_69_73_63_6f_20_53_79_73_74_65_6d_73_2c_20_49_6e_63_2e_0d_0a_43_6f_6d_70_69_6c_65_64_20_57_65_64_20_32_31_2d_41_70_72_2d_31_30_20_30_35_3a_33_33_20_62_79_20_70_72_6f_64_5f_72_65_6c_5f_74_65_61_6d
```
- snmpGet w Async

```
20:24:30.184125 IP 10.64.0.9.61054 > 10.64.0.250.snmp:  GetRequest(25)  system.sysName.0
20:24:30.186049 IP 10.64.0.9.55234 > 10.64.0.250.snmp:  GetRequest(25)  system.sysObjectID.0
20:24:30.187833 IP 10.64.0.9.56350 > 10.64.0.250.snmp:  GetRequest(25)  system.sysDescr.0
20:24:30.188658 IP 10.64.0.250.snmp > 10.64.0.9.61054:  GetResponse(44)  system.sysName.0="SW-Nuovo"
20:24:30.191639 IP 10.64.0.250.snmp > 10.64.0.9.55234:  GetResponse(34)  system.sysObjectID.0=E:cisco.1.563
20:24:30.191930 IP 10.64.0.250.snmp > 10.64.0.9.56350:  GetResponse(280)  system.sysDescr.0=43_69_73_63_6f_20_49_4f_53_20_53_6f_66_74_77_61_72_65_2c_20_43_33_35_36_30_20_53_6f_66_74_77_61_72_65_20_28_43_33_35_36_30_2d_49_50_53_45_52_56_49_43_45_53_4b_39_2d_4d_29_2c_20_56_65_72_73_69_6f_6e_20_31_32_2e_32_28_35_33_29_53_45_32_2c_20_52_45_4c_45_41_53_45_20_53_4f_46_54_57_41_52_45_20_28_66_63_33_29_0d_0a_54_65_63_68_6e_69_63_61_6c_20_53_75_70_70_6f_72_74_3a_20_68_74_74_70_3a_2f_2f_77_77_77_2e_63_69_73_63_6f_2e_63_6f_6d_2f_74_65_63_68_73_75_70_70_6f_72_74_0d_0a_43_6f_70_79_72_69_67_68_74_20_28_63_29_20_31_39_38_36_2d_32_30_31_30_20_62_79_20_43_69_73_63_6f_20_53_79_73_74_65_6d_73_2c_20_49_6e_63_2e_0d_0a_43_6f_6d_70_69_6c_65_64_20_57_65_64_20_32_31_2d_41_70_72_2d_31_30_20_30_35_3a_33_33_20_62_79_20_70_72_6f_64_5f_72_65_6c_5f_74_65_61_6d
```

demo
====
```
$ python snmpAsyncNG.py -r 10.64.0.250 -c public
WARNING: No route found for IPv6 destination :: (no default route?)
community: public

ospfAreaEntry 1.3.6.1.2.1.14.2.1

10.64.0.250 [ public ] ospfAreaId.0.0.0.0 - 0.0.0.0
10.64.0.250 [ public ] ospfAuthType.0.0.0.0 - 0
10.64.0.250 [ public ] ospfImportAsExtern.0.0.0.0 - 1
10.64.0.250 [ public ] ospfSpfRuns.0.0.0.0 - 3
10.64.0.250 [ public ] ospfAreaBdrRtrCount.0.0.0.0 - 0
10.64.0.250 [ public ] ospfAsBdrRtrCount.0.0.0.0 - 0
10.64.0.250 [ public ] ospfAreaLsaCount.0.0.0.0 - 1
10.64.0.250 [ public ] ospfAreaLsaCksumSum.0.0.0.0 - 63855
10.64.0.250 [ public ] ospfAreaSummary.0.0.0.0 - 2
10.64.0.250 [ public ] ospfAreaStatus.0.0.0.0 - 1
{
    "0.0.0.0": {
        "ospfAreaBdrRtrCount": 0,
        "ospfAreaId": "0.0.0.0",
        "ospfAreaLsaCksumSum": 63855,
        "ospfAreaLsaCount": 1,
        "ospfAreaStatus": 1,
        "ospfAreaSummary": 2,
        "ospfAsBdrRtrCount": 0,
        "ospfAuthType": 0,
        "ospfImportAsExtern": 1,
        "ospfSpfRuns": 3
    }
}
INFO:root:loading row to sql...DONE
+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
| ospfSpfRun | ospfAsBdrR | ospfAreaId | ospfAreaLs |     -      | ospfAuthTy | ospfAreaSt | ospfAreaLs | ospfImport | ospfAreaSu | ospfAreaBd |
|     s      |  trCount   |            |   aCount   |            |     pe     |    atus    | aCksumSum  |  AsExtern  |   mmary    | rRtrCount  |
+============+============+============+============+============+============+============+============+============+============+============+
| 3          | 0          | 0.0.0.0    | 1          | 0.0.0.0    | 0          | 1          | 63855      | 1          | 2          | 0          |
+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
===============
ifEntry 1.3.6.1.2.1.2.2.1

10.64.0.250 [ public ] ifIndex.1 - 1
10.64.0.250 [ public ] ifIndex.10001 - 10001
10.64.0.250 [ public ] ifIndex.10002 - 10002
10.64.0.250 [ public ] ifIndex.10003 - 10003
10.64.0.250 [ public ] ifIndex.10004 - 10004
10.64.0.250 [ public ] ifIndex.10005 - 10005
10.64.0.250 [ public ] ifIndex.10006 - 10006
10.64.0.250 [ public ] ifIndex.10007 - 10007
10.64.0.250 [ public ] ifIndex.10008 - 10008
10.64.0.250 [ public ] ifIndex.10009 - 10009
10.64.0.250 [ public ] ifIndex.10010 - 10010
10.64.0.250 [ public ] ifIndex.10011 - 10011
10.64.0.250 [ public ] ifIndex.10012 - 10012
10.64.0.250 [ public ] ifIndex.10013 - 10013
10.64.0.250 [ public ] ifIndex.10014 - 10014
10.64.0.250 [ public ] ifIndex.10015 - 10015
10.64.0.250 [ public ] ifIndex.10016 - 10016
10.64.0.250 [ public ] ifIndex.10017 - 10017
10.64.0.250 [ public ] ifIndex.10018 - 10018
10.64.0.250 [ public ] ifIndex.10019 - 10019
10.64.0.250 [ public ] ifIndex.10020 - 10020
10.64.0.250 [ public ] ifIndex.10021 - 10021
10.64.0.250 [ public ] ifIndex.10022 - 10022
10.64.0.250 [ public ] ifIndex.10023 - 10023
10.64.0.250 [ public ] ifIndex.10024 - 10024
10.64.0.250 [ public ] ifIndex.10101 - 10101
10.64.0.250 [ public ] ifIndex.10102 - 10102
10.64.0.250 [ public ] ifIndex.10501 - 10501
10.64.0.250 [ public ] ifDescr.1 - Vlan1
10.64.0.250 [ public ] ifDescr.10001 - FastEthernet0/1
10.64.0.250 [ public ] ifDescr.10002 - FastEthernet0/2
10.64.0.250 [ public ] ifDescr.10003 - FastEthernet0/3
10.64.0.250 [ public ] ifDescr.10004 - FastEthernet0/4
10.64.0.250 [ public ] ifDescr.10005 - FastEthernet0/5
10.64.0.250 [ public ] ifDescr.10006 - FastEthernet0/6
10.64.0.250 [ public ] ifDescr.10007 - FastEthernet0/7
10.64.0.250 [ public ] ifDescr.10008 - FastEthernet0/8
10.64.0.250 [ public ] ifDescr.10009 - FastEthernet0/9
10.64.0.250 [ public ] ifDescr.10010 - FastEthernet0/10
10.64.0.250 [ public ] ifDescr.10011 - FastEthernet0/11
10.64.0.250 [ public ] ifDescr.10012 - FastEthernet0/12
10.64.0.250 [ public ] ifDescr.10013 - FastEthernet0/13
10.64.0.250 [ public ] ifDescr.10014 - FastEthernet0/14
10.64.0.250 [ public ] ifDescr.10015 - FastEthernet0/15
10.64.0.250 [ public ] ifDescr.10016 - FastEthernet0/16
10.64.0.250 [ public ] ifDescr.10017 - FastEthernet0/17
10.64.0.250 [ public ] ifDescr.10018 - FastEthernet0/18
10.64.0.250 [ public ] ifDescr.10019 - FastEthernet0/19
10.64.0.250 [ public ] ifDescr.10020 - FastEthernet0/20
10.64.0.250 [ public ] ifDescr.10021 - FastEthernet0/21
10.64.0.250 [ public ] ifDescr.10022 - FastEthernet0/22
10.64.0.250 [ public ] ifDescr.10023 - FastEthernet0/23
10.64.0.250 [ public ] ifDescr.10024 - FastEthernet0/24
10.64.0.250 [ public ] ifDescr.10101 - GigabitEthernet0/1
10.64.0.250 [ public ] ifDescr.10102 - GigabitEthernet0/2
10.64.0.250 [ public ] ifDescr.10501 - Null0
10.64.0.250 [ public ] ifType.1 - 53
10.64.0.250 [ public ] ifType.10001 - 6
10.64.0.250 [ public ] ifType.10002 - 6
10.64.0.250 [ public ] ifType.10003 - 6
10.64.0.250 [ public ] ifType.10004 - 6
10.64.0.250 [ public ] ifType.10005 - 6
10.64.0.250 [ public ] ifType.10006 - 6
10.64.0.250 [ public ] ifType.10007 - 6
10.64.0.250 [ public ] ifType.10008 - 6
10.64.0.250 [ public ] ifType.10009 - 6
10.64.0.250 [ public ] ifType.10010 - 6
10.64.0.250 [ public ] ifType.10011 - 6
10.64.0.250 [ public ] ifType.10012 - 6
10.64.0.250 [ public ] ifType.10013 - 6
10.64.0.250 [ public ] ifType.10014 - 6
10.64.0.250 [ public ] ifType.10015 - 6
10.64.0.250 [ public ] ifType.10016 - 6
10.64.0.250 [ public ] ifType.10017 - 6
10.64.0.250 [ public ] ifType.10018 - 6
10.64.0.250 [ public ] ifType.10019 - 6
10.64.0.250 [ public ] ifType.10020 - 6
10.64.0.250 [ public ] ifType.10021 - 6
10.64.0.250 [ public ] ifType.10022 - 6
10.64.0.250 [ public ] ifType.10023 - 6
10.64.0.250 [ public ] ifType.10024 - 6
10.64.0.250 [ public ] ifType.10101 - 6
10.64.0.250 [ public ] ifType.10102 - 6
10.64.0.250 [ public ] ifType.10501 - 1
10.64.0.250 [ public ] ifMtu.1 - 1504
10.64.0.250 [ public ] ifMtu.10001 - 1504
10.64.0.250 [ public ] ifMtu.10002 - 1504
10.64.0.250 [ public ] ifMtu.10003 - 1504
10.64.0.250 [ public ] ifMtu.10004 - 1504
10.64.0.250 [ public ] ifMtu.10005 - 1504
10.64.0.250 [ public ] ifMtu.10006 - 1504
10.64.0.250 [ public ] ifMtu.10007 - 1504
10.64.0.250 [ public ] ifMtu.10008 - 1504
10.64.0.250 [ public ] ifMtu.10009 - 1504
10.64.0.250 [ public ] ifMtu.10010 - 1504
10.64.0.250 [ public ] ifMtu.10011 - 1504
10.64.0.250 [ public ] ifMtu.10012 - 1504
10.64.0.250 [ public ] ifMtu.10013 - 1504
10.64.0.250 [ public ] ifMtu.10014 - 1504
10.64.0.250 [ public ] ifMtu.10015 - 1504
10.64.0.250 [ public ] ifMtu.10016 - 1504
10.64.0.250 [ public ] ifMtu.10017 - 1504
10.64.0.250 [ public ] ifMtu.10018 - 1504
10.64.0.250 [ public ] ifMtu.10019 - 1504
10.64.0.250 [ public ] ifMtu.10020 - 1504
10.64.0.250 [ public ] ifMtu.10021 - 1504
10.64.0.250 [ public ] ifMtu.10022 - 1504
10.64.0.250 [ public ] ifMtu.10023 - 1504
10.64.0.250 [ public ] ifMtu.10024 - 1504
10.64.0.250 [ public ] ifMtu.10101 - 1504
10.64.0.250 [ public ] ifMtu.10102 - 1504
10.64.0.250 [ public ] ifMtu.10501 - 1500
10.64.0.250 [ public ] ifSpeed.1 - 1000000000
10.64.0.250 [ public ] ifSpeed.10001 - 100000000
10.64.0.250 [ public ] ifSpeed.10002 - 10000000
10.64.0.250 [ public ] ifSpeed.10003 - 100000000
10.64.0.250 [ public ] ifSpeed.10004 - 100000000
10.64.0.250 [ public ] ifSpeed.10005 - 10000000
10.64.0.250 [ public ] ifSpeed.10006 - 10000000
10.64.0.250 [ public ] ifSpeed.10007 - 100000000
10.64.0.250 [ public ] ifSpeed.10008 - 10000000
10.64.0.250 [ public ] ifSpeed.10009 - 100000000
10.64.0.250 [ public ] ifSpeed.10010 - 10000000
10.64.0.250 [ public ] ifSpeed.10011 - 10000000
10.64.0.250 [ public ] ifSpeed.10012 - 10000000
10.64.0.250 [ public ] ifSpeed.10013 - 10000000
10.64.0.250 [ public ] ifSpeed.10014 - 10000000
10.64.0.250 [ public ] ifSpeed.10015 - 10000000
10.64.0.250 [ public ] ifSpeed.10016 - 10000000
10.64.0.250 [ public ] ifSpeed.10017 - 10000000
10.64.0.250 [ public ] ifSpeed.10018 - 10000000
10.64.0.250 [ public ] ifSpeed.10019 - 10000000
10.64.0.250 [ public ] ifSpeed.10020 - 10000000
10.64.0.250 [ public ] ifSpeed.10021 - 10000000
10.64.0.250 [ public ] ifSpeed.10022 - 10000000
10.64.0.250 [ public ] ifSpeed.10023 - 10000000
10.64.0.250 [ public ] ifSpeed.10024 - 100000000
10.64.0.250 [ public ] ifSpeed.10101 - 10000000
10.64.0.250 [ public ] ifSpeed.10102 - 1000000000
10.64.0.250 [ public ] ifSpeed.10501 - 4294967295
10.64.0.250 [ public ] ifPhysAddress.1 - 00:1b:2b:7d:de:c0
10.64.0.250 [ public ] ifPhysAddress.10001 - 00:1b:2b:7d:de:83
10.64.0.250 [ public ] ifPhysAddress.10002 - 00:1b:2b:7d:de:84
10.64.0.250 [ public ] ifPhysAddress.10003 - 00:1b:2b:7d:de:85
10.64.0.250 [ public ] ifPhysAddress.10004 - 00:1b:2b:7d:de:86
10.64.0.250 [ public ] ifPhysAddress.10005 - 00:1b:2b:7d:de:87
10.64.0.250 [ public ] ifPhysAddress.10006 - 00:1b:2b:7d:de:88
10.64.0.250 [ public ] ifPhysAddress.10007 - 00:1b:2b:7d:de:89
10.64.0.250 [ public ] ifPhysAddress.10008 - 00:1b:2b:7d:de:8a
10.64.0.250 [ public ] ifPhysAddress.10009 - 00:1b:2b:7d:de:8b
10.64.0.250 [ public ] ifPhysAddress.10010 - 00:1b:2b:7d:de:8c
10.64.0.250 [ public ] ifPhysAddress.10011 - 00:1b:2b:7d:de:8d
10.64.0.250 [ public ] ifPhysAddress.10012 - 00:1b:2b:7d:de:8e
10.64.0.250 [ public ] ifPhysAddress.10013 - 00:1b:2b:7d:de:8f
10.64.0.250 [ public ] ifPhysAddress.10014 - 00:1b:2b:7d:de:90
10.64.0.250 [ public ] ifPhysAddress.10015 - 00:1b:2b:7d:de:91
10.64.0.250 [ public ] ifPhysAddress.10016 - 00:1b:2b:7d:de:92
10.64.0.250 [ public ] ifPhysAddress.10017 - 00:1b:2b:7d:de:93
10.64.0.250 [ public ] ifPhysAddress.10018 - 00:1b:2b:7d:de:94
10.64.0.250 [ public ] ifPhysAddress.10019 - 00:1b:2b:7d:de:95
10.64.0.250 [ public ] ifPhysAddress.10020 - 00:1b:2b:7d:de:96
10.64.0.250 [ public ] ifPhysAddress.10021 - 00:1b:2b:7d:de:97
10.64.0.250 [ public ] ifPhysAddress.10022 - 00:1b:2b:7d:de:98
10.64.0.250 [ public ] ifPhysAddress.10023 - 00:1b:2b:7d:de:99
10.64.0.250 [ public ] ifPhysAddress.10024 - 00:1b:2b:7d:de:9a
10.64.0.250 [ public ] ifPhysAddress.10101 - 00:1b:2b:7d:de:81
10.64.0.250 [ public ] ifPhysAddress.10102 - 00:1b:2b:7d:de:82
10.64.0.250 [ public ] ifPhysAddress.10501 - 
10.64.0.250 [ public ] ifAdminStatus.1 - 1
10.64.0.250 [ public ] ifAdminStatus.10001 - 1
10.64.0.250 [ public ] ifAdminStatus.10002 - 1
10.64.0.250 [ public ] ifAdminStatus.10003 - 1
10.64.0.250 [ public ] ifAdminStatus.10004 - 1
10.64.0.250 [ public ] ifAdminStatus.10005 - 1
10.64.0.250 [ public ] ifAdminStatus.10006 - 1
10.64.0.250 [ public ] ifAdminStatus.10007 - 1
10.64.0.250 [ public ] ifAdminStatus.10008 - 1
10.64.0.250 [ public ] ifAdminStatus.10009 - 1
10.64.0.250 [ public ] ifAdminStatus.10010 - 1
10.64.0.250 [ public ] ifAdminStatus.10011 - 1
10.64.0.250 [ public ] ifAdminStatus.10012 - 1
10.64.0.250 [ public ] ifAdminStatus.10013 - 1
10.64.0.250 [ public ] ifAdminStatus.10014 - 1
10.64.0.250 [ public ] ifAdminStatus.10015 - 1
10.64.0.250 [ public ] ifAdminStatus.10016 - 1
10.64.0.250 [ public ] ifAdminStatus.10017 - 1
10.64.0.250 [ public ] ifAdminStatus.10018 - 1
10.64.0.250 [ public ] ifAdminStatus.10019 - 1
10.64.0.250 [ public ] ifAdminStatus.10020 - 1
10.64.0.250 [ public ] ifAdminStatus.10021 - 1
10.64.0.250 [ public ] ifAdminStatus.10022 - 1
10.64.0.250 [ public ] ifAdminStatus.10023 - 1
10.64.0.250 [ public ] ifAdminStatus.10024 - 1
10.64.0.250 [ public ] ifAdminStatus.10101 - 1
10.64.0.250 [ public ] ifAdminStatus.10102 - 1
10.64.0.250 [ public ] ifAdminStatus.10501 - 1
10.64.0.250 [ public ] ifOperStatus.1 - 1
10.64.0.250 [ public ] ifOperStatus.10001 - 1
10.64.0.250 [ public ] ifOperStatus.10002 - 2
10.64.0.250 [ public ] ifOperStatus.10003 - 1
10.64.0.250 [ public ] ifOperStatus.10004 - 1
10.64.0.250 [ public ] ifOperStatus.10005 - 2
10.64.0.250 [ public ] ifOperStatus.10006 - 2
10.64.0.250 [ public ] ifOperStatus.10007 - 1
10.64.0.250 [ public ] ifOperStatus.10008 - 2
10.64.0.250 [ public ] ifOperStatus.10009 - 2
10.64.0.250 [ public ] ifOperStatus.10010 - 1
10.64.0.250 [ public ] ifOperStatus.10011 - 2
10.64.0.250 [ public ] ifOperStatus.10012 - 2
10.64.0.250 [ public ] ifOperStatus.10013 - 2
10.64.0.250 [ public ] ifOperStatus.10014 - 2
10.64.0.250 [ public ] ifOperStatus.10015 - 2
10.64.0.250 [ public ] ifOperStatus.10016 - 2
10.64.0.250 [ public ] ifOperStatus.10017 - 2
10.64.0.250 [ public ] ifOperStatus.10018 - 2
10.64.0.250 [ public ] ifOperStatus.10019 - 2
10.64.0.250 [ public ] ifOperStatus.10020 - 2
10.64.0.250 [ public ] ifOperStatus.10021 - 2
10.64.0.250 [ public ] ifOperStatus.10022 - 2
10.64.0.250 [ public ] ifOperStatus.10023 - 2
10.64.0.250 [ public ] ifOperStatus.10024 - 1
10.64.0.250 [ public ] ifOperStatus.10101 - 2
10.64.0.250 [ public ] ifOperStatus.10102 - 1
10.64.0.250 [ public ] ifOperStatus.10501 - 1
10.64.0.250 [ public ] ifLastChange.1 - 4851
10.64.0.250 [ public ] ifLastChange.10001 - 5672
10.64.0.250 [ public ] ifLastChange.10002 - 4471
10.64.0.250 [ public ] ifLastChange.10003 - 409096432
10.64.0.250 [ public ] ifLastChange.10004 - 539949949
10.64.0.250 [ public ] ifLastChange.10005 - 4471
10.64.0.250 [ public ] ifLastChange.10006 - 4471
10.64.0.250 [ public ] ifLastChange.10007 - 385722073
10.64.0.250 [ public ] ifLastChange.10008 - 4471
10.64.0.250 [ public ] ifLastChange.10009 - 530061102
10.64.0.250 [ public ] ifLastChange.10010 - 138591848
10.64.0.250 [ public ] ifLastChange.10011 - 4471
10.64.0.250 [ public ] ifLastChange.10012 - 4471
10.64.0.250 [ public ] ifLastChange.10013 - 4471
10.64.0.250 [ public ] ifLastChange.10014 - 4471
10.64.0.250 [ public ] ifLastChange.10015 - 4471
10.64.0.250 [ public ] ifLastChange.10016 - 4471
10.64.0.250 [ public ] ifLastChange.10017 - 4471
10.64.0.250 [ public ] ifLastChange.10018 - 4471
10.64.0.250 [ public ] ifLastChange.10019 - 4471
10.64.0.250 [ public ] ifLastChange.10020 - 4472
10.64.0.250 [ public ] ifLastChange.10021 - 4472
10.64.0.250 [ public ] ifLastChange.10022 - 4472
10.64.0.250 [ public ] ifLastChange.10023 - 4472
10.64.0.250 [ public ] ifLastChange.10024 - 5043
10.64.0.250 [ public ] ifLastChange.10101 - 4471
10.64.0.250 [ public ] ifLastChange.10102 - 5230
10.64.0.250 [ public ] ifLastChange.10501 - 0
10.64.0.250 [ public ] ifInOctets.1 - 1223803512
10.64.0.250 [ public ] ifInOctets.10001 - 3809515778
10.64.0.250 [ public ] ifInOctets.10002 - 0
10.64.0.250 [ public ] ifInOctets.10003 - 2499447721
10.64.0.250 [ public ] ifInOctets.10004 - 212000556
10.64.0.250 [ public ] ifInOctets.10005 - 0
10.64.0.250 [ public ] ifInOctets.10006 - 0
10.64.0.250 [ public ] ifInOctets.10007 - 2422834962
10.64.0.250 [ public ] ifInOctets.10008 - 0
10.64.0.250 [ public ] ifInOctets.10009 - 2695850
10.64.0.250 [ public ] ifInOctets.10010 - 67468594
10.64.0.250 [ public ] ifInOctets.10011 - 0
10.64.0.250 [ public ] ifInOctets.10012 - 0
10.64.0.250 [ public ] ifInOctets.10013 - 0
10.64.0.250 [ public ] ifInOctets.10014 - 0
10.64.0.250 [ public ] ifInOctets.10015 - 0
10.64.0.250 [ public ] ifInOctets.10016 - 0
10.64.0.250 [ public ] ifInOctets.10017 - 0
10.64.0.250 [ public ] ifInOctets.10018 - 0
10.64.0.250 [ public ] ifInOctets.10019 - 0
10.64.0.250 [ public ] ifInOctets.10020 - 0
10.64.0.250 [ public ] ifInOctets.10021 - 0
10.64.0.250 [ public ] ifInOctets.10022 - 0
10.64.0.250 [ public ] ifInOctets.10023 - 0
10.64.0.250 [ public ] ifInOctets.10024 - 39382893
10.64.0.250 [ public ] ifInOctets.10101 - 0
10.64.0.250 [ public ] ifInOctets.10102 - 3613528872
10.64.0.250 [ public ] ifInOctets.10501 - 0
10.64.0.250 [ public ] ifInUcastPkts.1 - 16045487
10.64.0.250 [ public ] ifInUcastPkts.10001 - 11809991
10.64.0.250 [ public ] ifInUcastPkts.10002 - 0
10.64.0.250 [ public ] ifInUcastPkts.10003 - 173803850
10.64.0.250 [ public ] ifInUcastPkts.10004 - 536977
10.64.0.250 [ public ] ifInUcastPkts.10005 - 0
10.64.0.250 [ public ] ifInUcastPkts.10006 - 0
10.64.0.250 [ public ] ifInUcastPkts.10007 - 447538
10.64.0.250 [ public ] ifInUcastPkts.10008 - 0
10.64.0.250 [ public ] ifInUcastPkts.10009 - 12606
10.64.0.250 [ public ] ifInUcastPkts.10010 - 505373
10.64.0.250 [ public ] ifInUcastPkts.10011 - 0
10.64.0.250 [ public ] ifInUcastPkts.10012 - 0
10.64.0.250 [ public ] ifInUcastPkts.10013 - 0
10.64.0.250 [ public ] ifInUcastPkts.10014 - 0
10.64.0.250 [ public ] ifInUcastPkts.10015 - 0
10.64.0.250 [ public ] ifInUcastPkts.10016 - 0
10.64.0.250 [ public ] ifInUcastPkts.10017 - 0
10.64.0.250 [ public ] ifInUcastPkts.10018 - 0
10.64.0.250 [ public ] ifInUcastPkts.10019 - 0
10.64.0.250 [ public ] ifInUcastPkts.10020 - 0
10.64.0.250 [ public ] ifInUcastPkts.10021 - 0
10.64.0.250 [ public ] ifInUcastPkts.10022 - 0
10.64.0.250 [ public ] ifInUcastPkts.10023 - 0
10.64.0.250 [ public ] ifInUcastPkts.10024 - 297626139
10.64.0.250 [ public ] ifInUcastPkts.10101 - 0
10.64.0.250 [ public ] ifInUcastPkts.10102 - 8723911
10.64.0.250 [ public ] ifInUcastPkts.10501 - 0
10.64.0.250 [ public ] ifInDiscards.1 - 0
10.64.0.250 [ public ] ifInDiscards.10001 - 0
10.64.0.250 [ public ] ifInDiscards.10002 - 0
10.64.0.250 [ public ] ifInDiscards.10003 - 0
10.64.0.250 [ public ] ifInDiscards.10004 - 0
10.64.0.250 [ public ] ifInDiscards.10005 - 0
10.64.0.250 [ public ] ifInDiscards.10006 - 0
10.64.0.250 [ public ] ifInDiscards.10007 - 0
10.64.0.250 [ public ] ifInDiscards.10008 - 0
10.64.0.250 [ public ] ifInDiscards.10009 - 0
10.64.0.250 [ public ] ifInDiscards.10010 - 0
10.64.0.250 [ public ] ifInDiscards.10011 - 0
10.64.0.250 [ public ] ifInDiscards.10012 - 0
10.64.0.250 [ public ] ifInDiscards.10013 - 0
10.64.0.250 [ public ] ifInDiscards.10014 - 0
10.64.0.250 [ public ] ifInDiscards.10015 - 0
10.64.0.250 [ public ] ifInDiscards.10016 - 0
10.64.0.250 [ public ] ifInDiscards.10017 - 0
10.64.0.250 [ public ] ifInDiscards.10018 - 0
10.64.0.250 [ public ] ifInDiscards.10019 - 0
10.64.0.250 [ public ] ifInDiscards.10020 - 0
10.64.0.250 [ public ] ifInDiscards.10021 - 0
10.64.0.250 [ public ] ifInDiscards.10022 - 0
10.64.0.250 [ public ] ifInDiscards.10023 - 0
10.64.0.250 [ public ] ifInDiscards.10024 - 0
10.64.0.250 [ public ] ifInDiscards.10101 - 0
10.64.0.250 [ public ] ifInDiscards.10102 - 0
10.64.0.250 [ public ] ifInDiscards.10501 - 0
10.64.0.250 [ public ] ifInErrors.1 - 0
10.64.0.250 [ public ] ifInErrors.10001 - 0
10.64.0.250 [ public ] ifInErrors.10002 - 0
10.64.0.250 [ public ] ifInErrors.10003 - 0
10.64.0.250 [ public ] ifInErrors.10004 - 0
10.64.0.250 [ public ] ifInErrors.10005 - 0
10.64.0.250 [ public ] ifInErrors.10006 - 0
10.64.0.250 [ public ] ifInErrors.10007 - 0
10.64.0.250 [ public ] ifInErrors.10008 - 0
10.64.0.250 [ public ] ifInErrors.10009 - 0
10.64.0.250 [ public ] ifInErrors.10010 - 0
10.64.0.250 [ public ] ifInErrors.10011 - 0
10.64.0.250 [ public ] ifInErrors.10012 - 0
10.64.0.250 [ public ] ifInErrors.10013 - 0
10.64.0.250 [ public ] ifInErrors.10014 - 0
10.64.0.250 [ public ] ifInErrors.10015 - 0
10.64.0.250 [ public ] ifInErrors.10016 - 0
10.64.0.250 [ public ] ifInErrors.10017 - 0
10.64.0.250 [ public ] ifInErrors.10018 - 0
10.64.0.250 [ public ] ifInErrors.10019 - 0
10.64.0.250 [ public ] ifInErrors.10020 - 0
10.64.0.250 [ public ] ifInErrors.10021 - 0
10.64.0.250 [ public ] ifInErrors.10022 - 0
10.64.0.250 [ public ] ifInErrors.10023 - 0
10.64.0.250 [ public ] ifInErrors.10024 - 0
10.64.0.250 [ public ] ifInErrors.10101 - 0
10.64.0.250 [ public ] ifInErrors.10102 - 0
10.64.0.250 [ public ] ifInErrors.10501 - 0
10.64.0.250 [ public ] ifInUnknownProtos.1 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10001 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10002 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10003 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10004 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10005 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10006 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10007 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10008 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10009 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10010 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10011 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10012 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10013 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10014 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10015 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10016 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10017 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10018 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10019 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10020 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10021 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10022 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10023 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10024 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10101 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10102 - 0
10.64.0.250 [ public ] ifInUnknownProtos.10501 - 0
10.64.0.250 [ public ] ifOutOctets.1 - 13285001
10.64.0.250 [ public ] ifOutOctets.10001 - 3639984813
10.64.0.250 [ public ] ifOutOctets.10002 - 0
10.64.0.250 [ public ] ifOutOctets.10003 - 1997256181
10.64.0.250 [ public ] ifOutOctets.10004 - 835805572
10.64.0.250 [ public ] ifOutOctets.10005 - 0
10.64.0.250 [ public ] ifOutOctets.10006 - 0
10.64.0.250 [ public ] ifOutOctets.10007 - 2247659322
10.64.0.250 [ public ] ifOutOctets.10008 - 0
10.64.0.250 [ public ] ifOutOctets.10009 - 8961297
10.64.0.250 [ public ] ifOutOctets.10010 - 3562483006
10.64.0.250 [ public ] ifOutOctets.10011 - 0
10.64.0.250 [ public ] ifOutOctets.10012 - 0
10.64.0.250 [ public ] ifOutOctets.10013 - 0
10.64.0.250 [ public ] ifOutOctets.10014 - 0
10.64.0.250 [ public ] ifOutOctets.10015 - 0
10.64.0.250 [ public ] ifOutOctets.10016 - 0
10.64.0.250 [ public ] ifOutOctets.10017 - 0
10.64.0.250 [ public ] ifOutOctets.10018 - 0
10.64.0.250 [ public ] ifOutOctets.10019 - 0
10.64.0.250 [ public ] ifOutOctets.10020 - 0
10.64.0.250 [ public ] ifOutOctets.10021 - 0
10.64.0.250 [ public ] ifOutOctets.10022 - 0
10.64.0.250 [ public ] ifOutOctets.10023 - 0
10.64.0.250 [ public ] ifOutOctets.10024 - 1014402546
10.64.0.250 [ public ] ifOutOctets.10101 - 0
10.64.0.250 [ public ] ifOutOctets.10102 - 25302228
10.64.0.250 [ public ] ifOutOctets.10501 - 0
10.64.0.250 [ public ] ifOutUcastPkts.1 - 140665
10.64.0.250 [ public ] ifOutUcastPkts.10001 - 13059807
10.64.0.250 [ public ] ifOutUcastPkts.10002 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10003 - 291643668
10.64.0.250 [ public ] ifOutUcastPkts.10004 - 222910
10.64.0.250 [ public ] ifOutUcastPkts.10005 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10006 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10007 - 671005
10.64.0.250 [ public ] ifOutUcastPkts.10008 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10009 - 13940
10.64.0.250 [ public ] ifOutUcastPkts.10010 - 529493
10.64.0.250 [ public ] ifOutUcastPkts.10011 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10012 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10013 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10014 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10015 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10016 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10017 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10018 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10019 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10020 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10021 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10022 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10023 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10024 - 186847014
10.64.0.250 [ public ] ifOutUcastPkts.10101 - 0
10.64.0.250 [ public ] ifOutUcastPkts.10102 - 1968435
10.64.0.250 [ public ] ifOutUcastPkts.10501 - 0
10.64.0.250 [ public ] ifOutDiscards.1 - 0
10.64.0.250 [ public ] ifOutDiscards.10001 - 0
10.64.0.250 [ public ] ifOutDiscards.10002 - 0
10.64.0.250 [ public ] ifOutDiscards.10003 - 0
10.64.0.250 [ public ] ifOutDiscards.10004 - 0
10.64.0.250 [ public ] ifOutDiscards.10005 - 0
10.64.0.250 [ public ] ifOutDiscards.10006 - 0
10.64.0.250 [ public ] ifOutDiscards.10007 - 0
10.64.0.250 [ public ] ifOutDiscards.10008 - 0
10.64.0.250 [ public ] ifOutDiscards.10009 - 0
10.64.0.250 [ public ] ifOutDiscards.10010 - 0
10.64.0.250 [ public ] ifOutDiscards.10011 - 0
10.64.0.250 [ public ] ifOutDiscards.10012 - 0
10.64.0.250 [ public ] ifOutDiscards.10013 - 0
10.64.0.250 [ public ] ifOutDiscards.10014 - 0
10.64.0.250 [ public ] ifOutDiscards.10015 - 0
10.64.0.250 [ public ] ifOutDiscards.10016 - 0
10.64.0.250 [ public ] ifOutDiscards.10017 - 0
10.64.0.250 [ public ] ifOutDiscards.10018 - 0
10.64.0.250 [ public ] ifOutDiscards.10019 - 0
10.64.0.250 [ public ] ifOutDiscards.10020 - 0
10.64.0.250 [ public ] ifOutDiscards.10021 - 0
10.64.0.250 [ public ] ifOutDiscards.10022 - 0
10.64.0.250 [ public ] ifOutDiscards.10023 - 0
10.64.0.250 [ public ] ifOutDiscards.10024 - 0
10.64.0.250 [ public ] ifOutDiscards.10101 - 0
10.64.0.250 [ public ] ifOutDiscards.10102 - 0
10.64.0.250 [ public ] ifOutDiscards.10501 - 0
10.64.0.250 [ public ] ifOutErrors.1 - 0
10.64.0.250 [ public ] ifOutErrors.10001 - 0
10.64.0.250 [ public ] ifOutErrors.10002 - 0
10.64.0.250 [ public ] ifOutErrors.10003 - 0
10.64.0.250 [ public ] ifOutErrors.10004 - 0
10.64.0.250 [ public ] ifOutErrors.10005 - 0
10.64.0.250 [ public ] ifOutErrors.10006 - 0
10.64.0.250 [ public ] ifOutErrors.10007 - 0
10.64.0.250 [ public ] ifOutErrors.10008 - 0
10.64.0.250 [ public ] ifOutErrors.10009 - 0
10.64.0.250 [ public ] ifOutErrors.10010 - 0
10.64.0.250 [ public ] ifOutErrors.10011 - 0
10.64.0.250 [ public ] ifOutErrors.10012 - 0
10.64.0.250 [ public ] ifOutErrors.10013 - 0
10.64.0.250 [ public ] ifOutErrors.10014 - 0
10.64.0.250 [ public ] ifOutErrors.10015 - 0
10.64.0.250 [ public ] ifOutErrors.10016 - 0
10.64.0.250 [ public ] ifOutErrors.10017 - 0
10.64.0.250 [ public ] ifOutErrors.10018 - 0
10.64.0.250 [ public ] ifOutErrors.10019 - 0
10.64.0.250 [ public ] ifOutErrors.10020 - 0
10.64.0.250 [ public ] ifOutErrors.10021 - 0
10.64.0.250 [ public ] ifOutErrors.10022 - 0
10.64.0.250 [ public ] ifOutErrors.10023 - 0
10.64.0.250 [ public ] ifOutErrors.10024 - 0
10.64.0.250 [ public ] ifOutErrors.10101 - 0
10.64.0.250 [ public ] ifOutErrors.10102 - 0
10.64.0.250 [ public ] ifOutErrors.10501 - 0
{
    "1": {
        "ifAdminStatus": 1,
        "ifDescr": "Vlan1",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 1223803512,
        "ifInUcastPkts": 16045487,
        "ifInUnknownProtos": 0,
        "ifIndex": 1,
        "ifLastChange": 4851,
        "ifMtu": 1504,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 13285001,
        "ifOutUcastPkts": 140665,
        "ifPhysAddress": "00:1b:2b:7d:de:c0",
        "ifSpeed": 1000000000,
        "ifType": 53
    },
    "10001": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/1",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 3809515778,
        "ifInUcastPkts": 11809991,
        "ifInUnknownProtos": 0,
        "ifIndex": 10001,
        "ifLastChange": 5672,
        "ifMtu": 1504,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 3639984813,
        "ifOutUcastPkts": 13059807,
        "ifPhysAddress": "00:1b:2b:7d:de:83",
        "ifSpeed": 100000000,
        "ifType": 6
    },
    "10002": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/2",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10002,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:84",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10003": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/3",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 2499447721,
        "ifInUcastPkts": 173803850,
        "ifInUnknownProtos": 0,
        "ifIndex": 10003,
        "ifLastChange": 409096432,
        "ifMtu": 1504,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 1997256181,
        "ifOutUcastPkts": 291643668,
        "ifPhysAddress": "00:1b:2b:7d:de:85",
        "ifSpeed": 100000000,
        "ifType": 6
    },
    "10004": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/4",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 212000556,
        "ifInUcastPkts": 536977,
        "ifInUnknownProtos": 0,
        "ifIndex": 10004,
        "ifLastChange": 539949949,
        "ifMtu": 1504,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 835805572,
        "ifOutUcastPkts": 222910,
        "ifPhysAddress": "00:1b:2b:7d:de:86",
        "ifSpeed": 100000000,
        "ifType": 6
    },
    "10005": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/5",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10005,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:87",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10006": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/6",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10006,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:88",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10007": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/7",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 2422834962,
        "ifInUcastPkts": 447538,
        "ifInUnknownProtos": 0,
        "ifIndex": 10007,
        "ifLastChange": 385722073,
        "ifMtu": 1504,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 2247659322,
        "ifOutUcastPkts": 671005,
        "ifPhysAddress": "00:1b:2b:7d:de:89",
        "ifSpeed": 100000000,
        "ifType": 6
    },
    "10008": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/8",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10008,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:8a",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10009": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/9",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 2695850,
        "ifInUcastPkts": 12606,
        "ifInUnknownProtos": 0,
        "ifIndex": 10009,
        "ifLastChange": 530061102,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 8961297,
        "ifOutUcastPkts": 13940,
        "ifPhysAddress": "00:1b:2b:7d:de:8b",
        "ifSpeed": 100000000,
        "ifType": 6
    },
    "10010": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/10",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 67468594,
        "ifInUcastPkts": 505373,
        "ifInUnknownProtos": 0,
        "ifIndex": 10010,
        "ifLastChange": 138591848,
        "ifMtu": 1504,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 3562483006,
        "ifOutUcastPkts": 529493,
        "ifPhysAddress": "00:1b:2b:7d:de:8c",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10011": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/11",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10011,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:8d",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10012": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/12",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10012,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:8e",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10013": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/13",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10013,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:8f",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10014": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/14",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10014,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:90",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10015": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/15",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10015,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:91",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10016": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/16",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10016,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:92",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10017": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/17",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10017,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:93",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10018": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/18",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10018,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:94",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10019": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/19",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10019,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:95",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10020": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/20",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10020,
        "ifLastChange": 4472,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:96",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10021": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/21",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10021,
        "ifLastChange": 4472,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:97",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10022": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/22",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10022,
        "ifLastChange": 4472,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:98",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10023": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/23",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10023,
        "ifLastChange": 4472,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:99",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10024": {
        "ifAdminStatus": 1,
        "ifDescr": "FastEthernet0/24",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 39382893,
        "ifInUcastPkts": 297626139,
        "ifInUnknownProtos": 0,
        "ifIndex": 10024,
        "ifLastChange": 5043,
        "ifMtu": 1504,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 1014402546,
        "ifOutUcastPkts": 186847014,
        "ifPhysAddress": "00:1b:2b:7d:de:9a",
        "ifSpeed": 100000000,
        "ifType": 6
    },
    "10101": {
        "ifAdminStatus": 1,
        "ifDescr": "GigabitEthernet0/1",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10101,
        "ifLastChange": 4471,
        "ifMtu": 1504,
        "ifOperStatus": 2,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "00:1b:2b:7d:de:81",
        "ifSpeed": 10000000,
        "ifType": 6
    },
    "10102": {
        "ifAdminStatus": 1,
        "ifDescr": "GigabitEthernet0/2",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 3613528872,
        "ifInUcastPkts": 8723911,
        "ifInUnknownProtos": 0,
        "ifIndex": 10102,
        "ifLastChange": 5230,
        "ifMtu": 1504,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 25302228,
        "ifOutUcastPkts": 1968435,
        "ifPhysAddress": "00:1b:2b:7d:de:82",
        "ifSpeed": 1000000000,
        "ifType": 6
    },
    "10501": {
        "ifAdminStatus": 1,
        "ifDescr": "Null0",
        "ifInDiscards": 0,
        "ifInErrors": 0,
        "ifInOctets": 0,
        "ifInUcastPkts": 0,
        "ifInUnknownProtos": 0,
        "ifIndex": 10501,
        "ifLastChange": 0,
        "ifMtu": 1500,
        "ifOperStatus": 1,
        "ifOutDiscards": 0,
        "ifOutErrors": 0,
        "ifOutOctets": 0,
        "ifOutUcastPkts": 0,
        "ifPhysAddress": "",
        "ifSpeed": 4294967295,
        "ifType": 1
    }
}
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
INFO:root:loading row to sql...DONE
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| ifSp | ifTy | ifIn | ifIn | ifOu |  -   | ifLa | ifPh | ifIn | ifIn | ifOu | ifAd | ifIn | ifDe | ifIn | ifOu | ifOu | ifMt | ifOp |
| eed  |  pe  | Octe | Disc | tErr |      | stCh | ysAd | Ucas | Erro | tOct | minS | Unkn | scr  | dex  | tUca | tDis |  u   | erSt |
|      |      |  ts  | ards | ors  |      | ange | dres | tPkt |  rs  | ets  | tatu | ownP |      |      | stPk | card |      | atus |
|      |      |      |      |      |      |      |  s   |  s   |      |      |  s   | roto |      |      |  ts  |  s   |      |      |
|      |      |      |      |      |      |      |      |      |      |      |      |  s   |      |      |      |      |      |      |
+======+======+======+======+======+======+======+======+======+======+======+======+======+======+======+======+======+======+======+
| 1000 | 6    | 2.12 | 0    | 0    | 1000 | 5.39 | 00:1 | 5369 | 0    | 8.35 | 1    | 0    | Fast | 1000 | 2229 | 0    | 1504 | 1    |
| 0000 |      | 0e+0 |      |      | 4    | 9e+0 | b:2b | 77   |      | 8e+0 |      |      | Ethe | 4    | 10   |      |      |      |
| 0    |      | 8    |      |      |      | 8    | :7d: |      |      | 8    |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/4  |      |      |      |      |      |
|      |      |      |      |      |      |      | 6    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1000 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1000 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 5    |      | b:2b |      |      |      |      |      | Ethe | 5    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/5  |      |      |      |      |      |
|      |      |      |      |      |      |      | 7    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1000 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1000 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 6    |      | b:2b |      |      |      |      |      | Ethe | 6    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/6  |      |      |      |      |      |
|      |      |      |      |      |      |      | 8    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 2.42 | 0    | 0    | 1000 | 3.85 | 00:1 | 4475 | 0    | 2.24 | 1    | 0    | Fast | 1000 | 6710 | 0    | 1504 | 1    |
| 0000 |      | 3e+0 |      |      | 7    | 7e+0 | b:2b | 38   |      | 8e+0 |      |      | Ethe | 7    | 05   |      |      |      |
| 0    |      | 9    |      |      |      | 8    | :7d: |      |      | 9    |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/7  |      |      |      |      |      |
|      |      |      |      |      |      |      | 9    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 3.81 | 0    | 0    | 1000 | 5672 | 00:1 | 1180 | 0    | 3.64 | 1    | 0    | Fast | 1000 | 1305 | 0    | 1504 | 1    |
| 0000 |      | 0e+0 |      |      | 1    |      | b:2b | 9991 |      | 0e+0 |      |      | Ethe | 1    | 9807 |      |      |      |
| 0    |      | 9    |      |      |      |      | :7d: |      |      | 9    |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/1  |      |      |      |      |      |
|      |      |      |      |      |      |      | 3    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1000 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1000 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 2    |      | b:2b |      |      |      |      |      | Ethe | 2    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/2  |      |      |      |      |      |
|      |      |      |      |      |      |      | 4    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 2.49 | 0    | 0    | 1000 | 4.09 | 00:1 | 1.73 | 0    | 1.99 | 1    | 0    | Fast | 1000 | 2.91 | 0    | 1504 | 1    |
| 0000 |      | 9e+0 |      |      | 3    | 1e+0 | b:2b | 8e+0 |      | 7e+0 |      |      | Ethe | 3    | 6e+0 |      |      |      |
| 0    |      | 9    |      |      |      | 8    | :7d: | 8    |      | 9    |      |      | rnet |      | 8    |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/3  |      |      |      |      |      |
|      |      |      |      |      |      |      | 5    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1000 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1000 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 8    |      | b:2b |      |      |      |      |      | Ethe | 8    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/8  |      |      |      |      |      |
|      |      |      |      |      |      |      | a    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 2695 | 0    | 0    | 1000 | 5.30 | 00:1 | 1260 | 0    | 8961 | 1    | 0    | Fast | 1000 | 1394 | 0    | 1504 | 2    |
| 0000 |      | 850  |      |      | 9    | 1e+0 | b:2b | 6    |      | 297  |      |      | Ethe | 9    | 0    |      |      |      |
| 0    |      |      |      |      |      | 8    | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/9  |      |      |      |      |      |
|      |      |      |      |      |      |      | b    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 4.29 | 1    | 0    | 0    | 0    | 1050 | 0    |      | 0    | 0    | 0    | 1    | 0    | Null | 1050 | 0    | 0    | 1500 | 1    |
| 5e+0 |      |      |      |      | 1    |      |      |      |      |      |      |      | 0    | 1    |      |      |      |      |
| 9    |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 3938 | 0    | 0    | 1002 | 5043 | 00:1 | 2.97 | 0    | 1.01 | 1    | 0    | Fast | 1002 | 1.86 | 0    | 1504 | 1    |
| 0000 |      | 2893 |      |      | 4    |      | b:2b | 6e+0 |      | 4e+0 |      |      | Ethe | 4    | 8e+0 |      |      |      |
| 0    |      |      |      |      |      |      | :7d: | 8    |      | 9    |      |      | rnet |      | 8    |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/24 |      |      |      |      |      |
|      |      |      |      |      |      |      | a    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1002 | 4472 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1002 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 2    |      | b:2b |      |      |      |      |      | Ethe | 2    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/22 |      |      |      |      |      |
|      |      |      |      |      |      |      | 8    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1002 | 4472 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1002 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 3    |      | b:2b |      |      |      |      |      | Ethe | 3    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/23 |      |      |      |      |      |
|      |      |      |      |      |      |      | 9    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1002 | 4472 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1002 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 0    |      | b:2b |      |      |      |      |      | Ethe | 0    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/20 |      |      |      |      |      |
|      |      |      |      |      |      |      | 6    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1002 | 4472 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1002 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 1    |      | b:2b |      |      |      |      |      | Ethe | 1    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/21 |      |      |      |      |      |
|      |      |      |      |      |      |      | 7    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1010 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Giga | 1010 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 1    |      | b:2b |      |      |      |      |      | bitE | 1    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | ther |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | net0 |      |      |      |      |      |
|      |      |      |      |      |      |      | 1    |      |      |      |      |      | /1   |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1.00 | 53   | 1.22 | 0    | 0    | 1    | 4851 | 00:1 | 1604 | 0    | 1328 | 1    | 0    | Vlan | 1    | 1406 | 0    | 1504 | 1    |
| 0e+0 |      | 4e+0 |      |      |      |      | b:2b | 5487 |      | 5001 |      |      | 1    |      | 65   |      |      |      |
| 9    |      | 9    |      |      |      |      | :7d: |      |      |      |      |      |      |      |      |      |      |      |
|      |      |      |      |      |      |      | de:c |      |      |      |      |      |      |      |      |      |      |      |
|      |      |      |      |      |      |      | 0    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1.00 | 6    | 3.61 | 0    | 0    | 1010 | 5230 | 00:1 | 8723 | 0    | 2530 | 1    | 0    | Giga | 1010 | 1968 | 0    | 1504 | 1    |
| 0e+0 |      | 4e+0 |      |      | 2    |      | b:2b | 911  |      | 2228 |      |      | bitE | 2    | 435  |      |      |      |
| 9    |      | 9    |      |      |      |      | :7d: |      |      |      |      |      | ther |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | net0 |      |      |      |      |      |
|      |      |      |      |      |      |      | 2    |      |      |      |      |      | /2   |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 9    |      | b:2b |      |      |      |      |      | Ethe | 9    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/19 |      |      |      |      |      |
|      |      |      |      |      |      |      | 5    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 8    |      | b:2b |      |      |      |      |      | Ethe | 8    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/18 |      |      |      |      |      |
|      |      |      |      |      |      |      | 4    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 3    |      | b:2b |      |      |      |      |      | Ethe | 3    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/13 |      |      |      |      |      |
|      |      |      |      |      |      |      | f    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 2    |      | b:2b |      |      |      |      |      | Ethe | 2    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/12 |      |      |      |      |      |
|      |      |      |      |      |      |      | e    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 1    |      | b:2b |      |      |      |      |      | Ethe | 1    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/11 |      |      |      |      |      |
|      |      |      |      |      |      |      | d    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 6746 | 0    | 0    | 1001 | 1.38 | 00:1 | 5053 | 0    | 3.56 | 1    | 0    | Fast | 1001 | 5294 | 0    | 1504 | 1    |
| 0000 |      | 8594 |      |      | 0    | 6e+0 | b:2b | 73   |      | 2e+0 |      |      | Ethe | 0    | 93   |      |      |      |
|      |      |      |      |      |      | 8    | :7d: |      |      | 9    |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:8 |      |      |      |      |      | 0/10 |      |      |      |      |      |
|      |      |      |      |      |      |      | c    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 7    |      | b:2b |      |      |      |      |      | Ethe | 7    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/17 |      |      |      |      |      |
|      |      |      |      |      |      |      | 3    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 6    |      | b:2b |      |      |      |      |      | Ethe | 6    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/16 |      |      |      |      |      |
|      |      |      |      |      |      |      | 2    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 5    |      | b:2b |      |      |      |      |      | Ethe | 5    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/15 |      |      |      |      |      |
|      |      |      |      |      |      |      | 1    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
| 1000 | 6    | 0    | 0    | 0    | 1001 | 4471 | 00:1 | 0    | 0    | 0    | 1    | 0    | Fast | 1001 | 0    | 0    | 1504 | 2    |
| 0000 |      |      |      |      | 4    |      | b:2b |      |      |      |      |      | Ethe | 4    |      |      |      |      |
|      |      |      |      |      |      |      | :7d: |      |      |      |      |      | rnet |      |      |      |      |      |
|      |      |      |      |      |      |      | de:9 |      |      |      |      |      | 0/14 |      |      |      |      |      |
|      |      |      |      |      |      |      | 0    |      |      |      |      |      |      |      |      |      |      |      |
+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+------+
===============
ipAddrTable 1.3.6.1.2.1.4.20

10.64.0.250 [ public ] ipAdEntAddr.10.64.0.250 - 10.64.0.250
10.64.0.250 [ public ] ipAdEntIfIndex.10.64.0.250 - 1
10.64.0.250 [ public ] ipAdEntNetMask.10.64.0.250 - 255.224.0.0
10.64.0.250 [ public ] ipAdEntBcastAddr.10.64.0.250 - 1
10.64.0.250 [ public ] ipAdEntReasmMaxSize.10.64.0.250 - 18024
{
    "10.64.0.250": {
        "ipAdEntAddr": "10.64.0.250",
        "ipAdEntBcastAddr": 1,
        "ipAdEntIfIndex": 1,
        "ipAdEntNetMask": "255.224.0.0",
        "ipAdEntReasmMaxSize": 18024
    }
}
INFO:root:loading row to sql...DONE
+-------------+----------------+-------------+----------------+------------------+---------------------+
| ipAdEntAddr | ipAdEntIfIndex |      -      | ipAdEntNetMask | ipAdEntBcastAddr | ipAdEntReasmMaxSize |
+=============+================+=============+================+==================+=====================+
| 10.64.0.250 | 1              | 10.64.0.250 | 255.224.0.0    | 1                | 18024               |
+-------------+----------------+-------------+----------------+------------------+---------------------+
===============
ospfIfMetricEntry 1.3.6.1.2.1.14.8.1

10.64.0.250 [ public ] ospfIfMetricIpAddress.10.64.0.250.0.0 - 10.64.0.250
10.64.0.250 [ public ] ospfIfMetricAddressLessIf.10.64.0.250.0.0 - 0
10.64.0.250 [ public ] ospfIfMetricTOS.10.64.0.250.0.0 - 0
10.64.0.250 [ public ] ospfIfMetricValue.10.64.0.250.0.0 - 124
10.64.0.250 [ public ] ospfIfMetricStatus.10.64.0.250.0.0 - 1
{
    "10.64.0.250.0.0": {
        "ospfIfMetricAddressLessIf": 0,
        "ospfIfMetricIpAddress": "10.64.0.250",
        "ospfIfMetricStatus": 1,
        "ospfIfMetricTOS": 0,
        "ospfIfMetricValue": 124
    }
}
INFO:root:loading row to sql...DONE
+-------------------+-----------------------+------------------+-----------------+--------------------+---------------------------+
| ospfIfMetricValue | ospfIfMetricIpAddress |        -         | ospfIfMetricTOS | ospfIfMetricStatus | ospfIfMetricAddressLessIf |
+===================+=======================+==================+=================+====================+===========================+
| 124               | 10.64.0.250           | 10.64.0.250.0.0  | 0               | 1                  | 0                         |
+-------------------+-----------------------+------------------+-----------------+--------------------+---------------------------+

===============
ospfNbrEntry 1.3.6.1.2.1.14.10.1

{}
+---+
| - |
+===+
+---+
===============
sysName 1.3.6.1.2.1.1.5.0
sysObjectID 1.3.6.1.2.1.1.2.0
sysDescr 1.3.6.1.2.1.1.1.0
10.64.0.250 [ public ] sysName.0 - SW-Nuovo
10.64.0.250 [ public ] sysObjectID.0 - catalyst356024PS
10.64.0.250 [ public ] sysDescr.0 - Cisco IOS Software, C3560 Software (C3560-IPSERVICESK9-M), Version 12.2(53)SE2, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2010 by Cisco Systems, Inc.
Compiled Wed 21-Apr-10 05:33 by prod_rel_team
```
