import sys
from datetime import datetime
from scapy.all import sniff, DNS, DNSQR, conf

from categories import categorize
from db import init_db, insert_query


def handle(pkt):
    # only DNS questions (qr == 0), and only type A (IPv4) lookups,
    # so one lookup becomes one row instead of A + AAAA duplicates
    if pkt.haslayer(DNS) and pkt.haslayer(DNSQR) and pkt[DNS].qr == 0:
        if pkt[DNSQR].qtype != 1:
            return
        domain = pkt[DNSQR].qname.decode(errors="ignore").rstrip(".").lower()
        if not domain:
            return
        category = categorize(domain)
        insert_query(domain, category)
        print(f"{datetime.now():%H:%M:%S}  [{category}]  {domain}")


def main():
    init_db()
    iface = sys.argv[1] if len(sys.argv) > 1 else conf.iface
    print(f"Listening for DNS queries on {iface} (Ctrl+C to stop)")
    sniff(filter="udp port 53", prn=handle, store=False, iface=iface)


if __name__ == "__main__":
    main()
