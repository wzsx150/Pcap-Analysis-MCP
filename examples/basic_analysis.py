#!/usr/bin/env python3
"""
Basic PCAP Analysis Example

Demonstrates the core workflow for analyzing a PCAP file.
"""

import sys
sys.path.insert(0, '..')

from pcap_analysis_mcp import PCAPAnalysisMCP


def main():
    # Create MCP instance
    mcp = PCAPAnalysisMCP()
    
    # Check dependencies
    status = mcp.check_installation()
    print("=== Dependency Check ===")
    print(f"Ready: {status['ready']}")
    for dep, info in status['dependencies'].items():
        print(f"  {dep}: {'OK' if info['installed'] else 'MISSING'}")
    
    if not status['ready']:
        print(f"\nInstall required deps: {status['install_command']}")
        return
    
    # Load PCAP
    pcap_path = input("\nEnter PCAP path: ").strip()
    if not pcap_path:
        print("No path provided")
        return
    
    print(f"\nLoading {pcap_path}...")
    result = mcp.load_pcap(pcap_path)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Loaded {result['metadata']['total_packets']} packets")
    
    # Get summary
    print("\n=== Summary ===")
    summary = mcp.get_summary()
    print(f"Duration: {summary.get('duration_seconds', 0)} seconds")
    print(f"Unique IPs: {summary.get('unique_ips', 0)}")
    print(f"Protocols: {summary.get('protocols', {})}")
    
    # Detect port scanning
    print("\n=== Port Scan Detection ===")
    scans = mcp.detect_port_scan()
    if scans['scan_detected']:
        for scanner in scans['scanners']:
            print(f"  Scanner: {scanner['scanner_ip']} ({scanner['ports_scanned']} ports)")
    else:
        print("  No port scanning detected")
    
    # Detect web exploits
    print("\n=== Web Exploit Detection ===")
    exploits = mcp.detect_web_exploits()
    print(f"Exploits found: {exploits['exploits_detected']}")
    for finding in exploits.get('findings', []):
        print(f"  [{finding['severity'].upper()}] {finding['name']}")
        print(f"    Source: {finding['src']} -> {finding['dst']}")
    
    # Build attack timeline
    print("\n=== Attack Timeline ===")
    timeline = mcp.build_attack_timeline()
    for event in timeline.get('events', []):
        print(f"  [{event['phase']}] {event['type']} - {event.get('source', 'N/A')}")
    
    # Extract IoCs
    print("\n=== IoCs ===")
    iocs = mcp.extract_all_iocs()
    print(f"IPs: {len(iocs.get('ips', []))}")
    print(f"Domains: {len(iocs.get('domains', []))}")
    
    # Generate report
    print("\n=== Generating Report ===")
    report = mcp.generate_html_report("analysis_report.html")
    if report.get('success'):
        print(f"Report saved: {report['path']}")
    else:
        print(f"Report error: {report.get('error')}")
    
    # Export JSON
    json_export = mcp.export_findings_json("findings.json")
    if json_export.get('success'):
        print(f"JSON saved: {json_export['path']}")


if __name__ == "__main__":
    main()

