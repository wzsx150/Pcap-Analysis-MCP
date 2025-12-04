#!/usr/bin/env python3
"""
CTF Challenge Analysis Example

Quick workflow for analyzing PCAP files in CTF challenges.
"""

import sys
sys.path.insert(0, '..')

from pcap_analysis_mcp import PCAPAnalysisMCP


def analyze_ctf_pcap(pcap_path: str):
    """Run CTF-focused analysis"""
    mcp = PCAPAnalysisMCP()
    
    # Load
    result = mcp.load_pcap(pcap_path)
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"[+] Loaded {result['metadata']['total_packets']} packets")
    print(f"[+] Duration: {result['metadata']['duration_seconds']}s")
    
    # Quick recon check
    print("\n[*] Checking for reconnaissance...")
    scans = mcp.detect_port_scan(threshold=10)
    if scans['scan_detected']:
        print(f"[!] Port scan detected from: {scans['scanners'][0]['scanner_ip']}")
        print(f"    Ports scanned: {scans['scanners'][0]['ports_scanned']}")
    
    # Find first responder (often the target)
    first = mcp.get_first_responder()
    if first.get('ip'):
        print(f"[+] First responder: {first['ip']}:{first['port']}")
    
    # Check for exploits
    print("\n[*] Checking for exploits...")
    exploits = mcp.detect_web_exploits()
    if exploits['exploits_detected'] > 0:
        print(f"[!] Found {exploits['exploits_detected']} exploit(s):")
        for f in exploits['findings']:
            print(f"    - {f['name']} ({f['severity']})")
            print(f"      {f['src']} -> {f['dst']}")
    
    # Check for reverse shells
    print("\n[*] Checking for reverse shells...")
    shells = mcp.detect_reverse_shells()
    if shells['shells']:
        print(f"[!] Found {len(shells['shells'])} shell indicator(s):")
        for s in shells['shells']:
            print(f"    - {s['type']} at packet {s['index']}")
    
    # Check for C2 beacons
    print("\n[*] Checking for C2 beacons...")
    beacons = mcp.detect_c2_beacons()
    if beacons['beacons']:
        print(f"[!] Found {len(beacons['beacons'])} beacon(s):")
        for b in beacons['beacons']:
            print(f"    - {b['src']} -> {b['dst']}:{b['port']} (interval: {b['interval']}s)")
    
    # Check DNS for tunneling/exfil
    print("\n[*] Checking DNS...")
    dns = mcp.analyze_dns()
    print(f"[+] DNS queries: {dns['queries']}")
    if dns['suspicious_tunneling']:
        print(f"[!] Suspicious DNS (possible tunneling):")
        for s in dns['suspicious_tunneling'][:5]:
            print(f"    - {s['query'][:80]}...")
    
    # Extract credentials (FTP)
    print("\n[*] Checking for credentials...")
    ftp = mcp.analyze_ftp()
    if ftp['credentials']:
        print(f"[!] FTP credentials found:")
        for c in ftp['credentials']:
            print(f"    - {c['type']}: {c['value']}")
    
    # Search for common CTF patterns
    print("\n[*] Searching for flag patterns...")
    patterns = ['HTB\\{', 'FLAG\\{', 'flag\\{', 'CTF\\{', 'picoCTF\\{']
    for pattern in patterns:
        result = mcp.search_payload(pattern, limit=5)
        if result['matches'] > 0:
            print(f"[!] Found '{pattern}' pattern in {result['matches']} packet(s)")
    
    # Get unique domains
    print("\n[*] Domains observed:")
    unique = mcp.get_unique_values("domains")
    for domain in unique.get('domains', [])[:10]:
        print(f"    - {domain}")
    
    # MITRE mapping
    print("\n[*] MITRE ATT&CK techniques:")
    mitre = mcp.map_to_mitre()
    for t in mitre['techniques']:
        print(f"    - {t['id']}: {t['name']} ({t['tactic']})")
    
    # Timeline
    print("\n[*] Attack phases:")
    timeline = mcp.build_attack_timeline()
    for phase in timeline['phases']:
        print(f"    - {phase}")
    
    print("\n[+] Analysis complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ctf_challenge.py <pcap_file>")
        sys.exit(1)
    
    analyze_ctf_pcap(sys.argv[1])

