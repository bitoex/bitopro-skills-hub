# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it
**privately** via one of:

- **GitHub Security Advisory** (preferred): open a private advisory at
  <https://github.com/bitoex/bitopro-skills-hub/security/advisories/new>
- **BitoPro support**: <https://www.bitopro.com/> → Help / Contact, mark
  the subject with `[SECURITY][skills-hub]`

Response SLA:
- Acknowledgment within **3 business days**
- Initial assessment within **7 business days**
- Remediation timeline depends on severity (see below)

> Please **do not** open public GitHub issues for security vulnerabilities.
> Public disclosure before remediation puts our users at risk.

## Severity & Remediation Timeline

| Severity | Examples | Target Remediation |
|---|---|---|
| Critical | Trading API key leak, order execution bypass, supply-chain RCE | 24 hours |
| High | Authentication bypass, unauthorized order placement, brand impersonation on package registries | 7 days |
| Medium | Information disclosure, denial-of-service, weak audit logging | 30 days |
| Low | Hardening suggestions, documentation gaps | Best effort |

## Scope

### In Scope

- The `bitopro-skills-hub` repository (this repo)
- Skills published in this repo under `skills/bitopro/*` — currently
  `spot` and `market-intel`
- The `bitopro-trade-guard` hook (npm name: `@bitopro/trade-guard`)
- Supply-chain concerns:
  - Name-squatting on public package registries using `bitopro-*` or
    `@bitopro/*` names
  - Compromised dependencies in `bitopro-trade-guard/package.json`
  - Tampered git tags or releases
- HMAC-SHA384 signing implementations in skill references

### Out of Scope

- The BitoPro exchange API itself — please use BitoPro's official
  support channels at <https://www.bitopro.com/>
- Third-party platforms integrating our skills (ClawHub, OpenClaw runtime,
  Claude Code) — please report to the respective platform
- Social engineering against BitoPro staff
- Denial-of-service against BitoPro infrastructure
- Issues in transitive dev dependencies that don't impact skill security posture
- Unverified theoretical attacks without a working proof-of-concept

## Distribution Notice (Important)

This project's skills are distributed via:

- `git clone https://github.com/bitoex/bitopro-skills-hub.git`
- `npx clawhub install <skill-name>`

Skills are **NOT** distributed via the public npm registry. Any package
matching `bitopro-*` (without the `@bitopro/` scope) on public npm is
**unofficial** and may be malicious — **do not install it**.

The `@bitopro/trade-guard` hook package on npm is published exclusively from
this repository under our reserved npm organization.

The unscoped name `bitopro-trade-guard` on public npm is **not maintained by
us** — any version that has appeared under that unscoped name was unofficial
and may be malicious. Do not install a package matching the unscoped name;
use only `@bitopro/trade-guard` (with the `@bitopro/` scope) if you need to
reference the hook from npm at all.

## Coordinated Disclosure Process

1. Reporter sends details through one of the private channels listed in
   [Reporting a Vulnerability](#reporting-a-vulnerability) above
2. We acknowledge within 3 business days
3. We triage, reproduce, and assign severity
4. We develop and verify a fix
5. We coordinate disclosure timing with the reporter
6. After remediation, we publish a security advisory and credit the reporter
   (unless anonymity is requested)

## Hall of Fame

We thank the following researchers for responsibly disclosed vulnerabilities:

<!-- Add credits here as disclosures complete -->

- _Listings coming soon._

## Bug Bounty

We do not currently operate a formal paid bug bounty program for the skills hub.
Researchers reporting valid in-scope issues will be credited in this file (with
permission) and may receive small tokens of appreciation at our discretion.

The BitoPro exchange platform itself runs a separate bounty program — see
<https://www.bitopro.com/security> for details.
