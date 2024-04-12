# snmpwalk -Cc -c public -v2c 192.168.0.104 -- получить все oid в человекочитаемом виде
# snmpwalk -Cc -c public -v2c -On 192.168.0.104 -- получить все oid

# .1.3.6.1.4.1.2021.10.1.3.1 -- cpu usage 1 min
# .1.3.6.1.4.1.2021.10.1.3.2 -- cpu usage 5 min
# .1.3.6.1.4.1.2021.10.1.3.3 -- cpu usage 10 min
# HOST-RESOURCES-MIB::hrDeviceDescr.196608 -- processor name
# snmpwalk -v 2c -c read_only_community_string localhost 1.3.6.1.4.1.2021.4 - RAM
# snmpwalk -v 2c -c read_only_community_string localhost HOST-RESOURCES-MIB::hrProcessorFrwID


from time import sleep
import time
import snmp
from hurry.filesize import size, si

client = snmp.SNMPClient('localhost')
# print(client.check_connection())
# print("Cpu usage 1 min:", client.get_cpu_usage_1min())
# print("Cpu usage 5 min:", client.get_cpu_usage_5min())
# print("Cpu usage 15 min:", client.get_cpu_usage_10min())
print(client.get_internet_traffic_out())
print(client.get_internet_traffic_in())

# print(int(client.get_temp()) / 1000, "°C")
# print(size(int(client.get_total_ram()) * 1000))
# print(size(int(client.get_avail_ram()) * 1000))
# print(size(int(client.get_cached_ram()) * 1000))

print(client.get_cpu_count())

