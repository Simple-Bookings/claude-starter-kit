# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **Do not** open a public issue
2. Email the maintainers directly
3. Include steps to reproduce
4. Allow time for a fix before disclosure

We aim to respond within 48 hours and provide a fix within 7 days for critical issues.

## Security Considerations

CSK2 is a development tool that:

- Runs locally on your machine
- Does not collect or transmit data
- Has no network dependencies except for PyPI (upgrades)

### API Keys

When using Claude Code with CSK2:

- Never commit API keys to version control
- Use environment variables for sensitive data
- Review Claude's outputs before sharing code publicly
