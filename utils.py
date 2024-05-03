import re

def check_valid_ip(ip_string):
    aa = re.match(
            r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
            ip_string
    )
    if aa is None:
        return False
    return True

def kilobyte_to_gigabyte(kilobyte):
    return kilobyte / 1024 / 1024