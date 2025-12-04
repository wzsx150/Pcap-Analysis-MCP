# Changelog

## [1.0.0] - 2024-12-04

Initial release - POC for network forensics via MCP.

### Features
- 50+ analysis tools across 8 categories
- Attack detection (CVEs, scans, exploits)
- Timeline reconstruction with MITRE ATT&CK mapping
- IoC extraction and optional enrichment
- Protocol analysis (HTTP, DNS, SMB, FTP, SSH, RDP, SMTP, TLS)
- C2/reverse shell detection
- HTML report generation

### Detection Patterns
- CVE-2024-4577, CVE-2021-44228, CVE-2021-41773
- SQL injection, XSS, command injection, path traversal
- Webshells, SSRF, XXE, LFI, deserialization
- Reverse shell patterns (bash, netcat, python, powershell)
- C2 beacon detection
