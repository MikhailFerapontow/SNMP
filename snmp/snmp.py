from pysnmp.hlapi import *

class SNMPClient:
    def __init__(self, ip_address, community='read_only_community_string'):
        self.ip_address = ip_address
        self.community = community
        self.snmp_engine = SnmpEngine()

    def __get_snmp_request(self, oid: ObjectIdentity):
        iterator = getCmd(self.snmp_engine,
                   CommunityData(self.community, mpModel=1),
                  UdpTransportTarget((self.ip_address, 161), timeout=1, retries=5, tagList=''),
                  ContextData(),
                  ObjectType(oid))
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:
            print(errorIndication)
            return None
        elif errorStatus:
            print(f"{errorStatus.prettyPrint()} at {varBinds[int(errorIndex) - 1][0] if errorIndex else '?'}")
            return None
        else:
            return varBinds[0][1].prettyPrint()

    def get_cpu_usage_1min(self):
        return self.__get_snmp_request(ObjectIdentity('.1.3.6.1.4.1.2021.10.1.3.1'))

    def get_cpu_usage_5min(self):
        return self.__get_snmp_request(ObjectIdentity('.1.3.6.1.4.1.2021.10.1.3.2'))

    def get_cpu_usage_10min(self):
        return self.__get_snmp_request(ObjectIdentity('.1.3.6.1.4.1.2021.10.1.3.3'))

    def get_internet_traffic_out(self):
        return self.__get_snmp_request(ObjectIdentity("IF-MIB", "ifOutOctets", 2))

    def get_internet_traffic_in(self):
        return self.__get_snmp_request(ObjectIdentity("IF-MIB", "ifInOctets", 2))

    def get_cpu_temperature(self):
        return self.__get_snmp_request(ObjectIdentity("LM-SENSORS-MIB", "lmTempSensorsValue", 1))

    def get_total_ram(self):
        return self.__get_snmp_request(ObjectIdentity("UCD-SNMP-MIB", "memTotalReal", 0))

    def get_avail_ram(self):
        return self.__get_snmp_request(ObjectIdentity("UCD-SNMP-MIB", "memAvailReal", 0))

    def get_cached_ram(self):
        return self.__get_snmp_request(ObjectIdentity("UCD-SNMP-MIB", "memCached", 0))

    def get_buffer_ram(self):
        return self.__get_snmp_request(ObjectIdentity("UCD-SNMP-MIB", "memBuffer", 0))

    def get_shared_ram(self):
        return self.__get_snmp_request(ObjectIdentity("UCD-SNMP-MIB", "memShared", 0))

    def check_connection(self):
        val = self.__get_snmp_request(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0))
        return True if val else False

    def get_cpu_count(self):
        count = 0
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_address, 161)),
            ContextData(),
            ObjectType(ObjectIdentity("HOST-RESOURCES-MIB", "hrProcessorFrwID")),
            lexicographicMode=False
        ):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
                    )
                )
                break
            else:
                for _ in varBinds:
                    count += 1
        return count

