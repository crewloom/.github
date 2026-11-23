<p align="center"><img src="https://raw.githubusercontent.com/crewloom/.github/main/assets/crewloom-banner.svg" width="100%" alt="Crewloom: roles, memory and evidence for agent work" /></p>

# Crewloom

Practical tools for AI agent work. Built by Rumuze.

[العربية](README.ar.md) · [Product website](https://crewloom.org)

## Projects

Versions below are an audit snapshot from 2026-11-23, not a live deployment guarantee. Each component is versioned separately.

| Project | Published version | What is available |
| --- | --- | --- |
| [Core toolkit](https://github.com/crewloom/crewloom) | v0.9.24 | 47 specialist role guides, 24 registered tools, working-memory contracts, an MCP bridge and managed Docker execution. Apache-2.0. |
| [Operations bridge](https://github.com/crewloom/bridge) | v2.2.5 repository release | Telegram and Console adapters; OpenCode integration and generic CLI wrappers. Other channels require separate adapters. The legacy AgentGram npm package is a separate distribution; installation names still need review. MIT. |
| [Desktop Agent downloads](https://github.com/crewloom/crewloom.github.io/releases/latest) | v0.39.11 | Published desktop release. Private source versions may be newer; check release assets for platform availability. |
| Pulse research | Component versions differ | Private local-routing research. The active Rust engine is lexical. Trained research artifacts are separate from the integrated runtime; benchmarks must identify backend, dataset and hardware. |
| [Website](https://crewloom.org) | Source package 1.1.0 | English and Arabic product pages. Website source, deployed download metadata and Desktop releases have separate version identities. |

## Scope and limits

Role guides and working-memory contracts help structure agent work. They do not guarantee correct answers or prevent hallucinations.

Managed execution adds scoped isolation, declared inputs and outputs, and review evidence. These controls do not govern arbitrary agents with host access. See [Core enforcement boundaries](https://github.com/crewloom/crewloom/blob/main/documentation/ENFORCEMENT.md).

Local operation depends on the selected model provider, host and integrations. Cloud providers and remote communication channels have their own data handling. Working memory and logs can retain data locally. There is no blanket zero-retention, no-destruction or regulatory-compliance guarantee.

## Release information

Use each project's GitHub releases as its publication record. The [profile refresh workflow](https://github.com/crewloom/.github/actions/workflows/refresh-profile.yml) proposes release-table updates through a pull request; changes are not visible until merged. It does not synchronize every project version or the Arabic profile automatically.

<!-- releases:start -->
| Date | Release | Repository |
| --- | --- | --- |
| 2026-11-22 | Crewloom Bridge v2.2.5 | bridge |
| 2026-11-21 | Crewloom Core v0.9.24 | crewloom |
| 2026-11-21 | Crewloom Desktop Agent v0.39.11 | crewloom.github.io |
<!-- releases:end -->

## Enterprise inquiries

Contact [support@crewloom.org](mailto:support@crewloom.org) to discuss private deployments, custom roles and support requirements. Availability, deployment controls and service commitments must be agreed for the specific engagement.

## Security and community

[Security policy](https://github.com/crewloom/.github/blob/main/SECURITY.md) · [Code of conduct](https://github.com/crewloom/.github/blob/main/CODE_OF_CONDUCT.md)
