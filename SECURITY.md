# Security Policy

## Reporting Security Vulnerabilities


If you discover a security vulnerability in Midna, please help us by reporting it responsibly.

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing:
- **Maintainer Email**: [jasemmanita@viraxi.tech](mailto:jasemmanita@viraxi.tech)
- **Org Contact**: [contact@viraxi.tech](mailto:contact@viraxi.tech)
- **Subject**: `[SECURITY] Midna Vulnerability Report`

### What to Include

When reporting a security vulnerability, please include:

1. **Description**: A clear description of the vulnerability
2. **Impact**: What an attacker could achieve by exploiting this vulnerability
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Affected Versions**: Which versions of Midna are affected
5. **Mitigation**: Any workarounds or mitigations you've identified

### Our Commitment

- We will acknowledge receipt of your report within 48 hours
- We will provide a more detailed response within 7 days indicating our next steps
- We will keep you informed about our progress throughout the process
- We will credit you (if desired) once the issue is resolved

### Security Measures

Midna implements several security measures:

- **Automated Security Scanning**: Every commit is scanned with Bandit for security issues
- **Dependency Vulnerability Checks**: Weekly scans for known CVEs in dependencies
- **Secure Subprocess Execution**: All pip calls use explicit `shell=False`
- **Minimal Dependencies**: Only essential dependencies to reduce attack surface
- **Code Review**: All changes require review before merging

### Known Security Considerations

- Midna executes pip commands with user-controlled package names
- File operations are performed on user-specified paths
- Network requests are delegated to pip (no direct HTTP calls in Midna)

### Responsible Disclosure

We kindly ask that you:

- Give us reasonable time to fix the issue before public disclosure
- Avoid accessing or modifying user data
- Do not perform DoS attacks or degrade services
- Respect rate limits and other protective measures

Thank you for helping keep Midna and its users secure!