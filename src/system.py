import netifaces as ni

def get_ip():
    return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']