# Security Policy

At **Crewloom** (a [Rumuze](https://rumuze.com) initiative), security and privacy are fundamental principles in how we design, build, and distribute tools for autonomous and semi-autonomous AI agent systems.

## Supported Versions

We provide security updates and patches for the following versions:

| Project | Version | Supported |
| --- | --- | --- |
| **crewloom/crewloom** | `>= 1.0.0` | :white_check_mark: |
| **crewloom/bridge** | `>= 2.0.0` | :white_check_mark: |

## Reporting a Vulnerability

We take all security vulnerability reports seriously. If you discover a potential vulnerability in any Crewloom repository or package, please do **NOT** open a public issue.

Instead, please report it privately through one of the following methods:

1. **GitHub Private Vulnerability Reporting:**  
   Use the **Security** tab of the respective repository and click **"Report a vulnerability"**.
2. **Direct Security Email:**  
   Send an email to: **[security@rumuze.com](mailto:security@rumuze.com)** or **[support@rumuze.com](mailto:support@rumuze.com)** with the subject line `[SECURITY] Potential vulnerability in Crewloom`.

### What to Include in Your Report

To help us triage and resolve the issue quickly, please include:
- A clear description of the vulnerability and its potential impact.
- Step-by-step instructions or proof-of-concept (PoC) code to reproduce the issue.
- The component, repository, and version affected.
- Any suggested mitigations or fixes (if available).

### Response SLA

- **Acknowledgment:** Within 24-48 business hours.
- **Initial Assessment:** Within 3-5 business days.
- **Disclosure Policy:** We follow coordinated disclosure guidelines. We ask that you give us reasonable time to investigate and issue a patch before making any information public.

---

## Enterprise & Commercial Security Assurances

For organizations and enterprise teams deploying Crewloom in production environments:
- **Zero Data Retention:** Our open-source and on-premise components do not phone home or transmit agent working memory to external servers.
- **Isolated Execution:** All skill and role execution models are designed for air-gapped or VPC deployment.
- **Custom Security Audits:** Enterprise customers requiring formal audits or custom compliance sign-offs can contact **[enterprise@rumuze.com](mailto:support@rumuze.com)**.
