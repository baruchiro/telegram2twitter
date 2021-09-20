import os
import netifaces as ni

def get_ip():
    return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

def ping():
    router = '192.168.1.1'
    response = os.system('ping -c 1 ' + router)
    return response == 0
