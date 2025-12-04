# Security

## Disclaimer

This is a **proof-of-concept (POC) project** built for personal use. It is provided as-is with no guarantees, support, or active maintenance.

## Reporting Issues

If you find a security issue, feel free to open an issue on GitHub. There are no guarantees on response time or fixes - this is a personal project.

## Usage Considerations

### API Keys

If using IoC enrichment features:

```bash
# Use environment variables, don't hardcode
export VIRUSTOTAL_API_KEY="your-key"
export ABUSEIPDB_API_KEY="your-key"
```

### PCAP Files

- PCAP files can contain sensitive data (credentials, PII)
- Handle them appropriately for your use case

### General

- This tool executes regex against packet payloads
- Large files load into memory
- External API calls transmit IoC data
- Use your own judgment

## No Warranty

This software is provided "as is" without warranty of any kind. Use at your own risk.
