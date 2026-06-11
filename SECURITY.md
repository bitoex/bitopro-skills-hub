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

> **Never run `npm install bitopro-spot` / `bitopro-market-intel` /
> `bitopro-trade-guard` (or any other unscoped `bitopro-*` name).** Install
> skills only with `npx clawhub install <skill-name>` or `git clone` from
> this repository.

### The only official npm package

The single package we publish to npm is the hook **`@bitopro/trade-guard`**
(with the `@bitopro/` scope), published from this repository under our
reserved npm organization. If you ever need to reference the hook from npm,
use the scoped name **only**.

### Known unofficial / squatted package names

The skill names are **import-by-name identifiers**, and the unscoped forms
were unclaimed on public npm — a classic dependency-confusion exposure
(CWE-427 / CWE-829). The following unscoped names are **not ours**; treat any
package published under them as untrusted:

| Unscoped name (public npm) | Status (as of 2026-06-11) |
|---|---|
| `bitopro-spot` | **Squatted by a third party** — registered 2026-06-06 as a security-research PoC carrying an `install` lifecycle script. Not maintained by BitoPro. |
| `bitopro-market-intel` | **Squatted by a third party** — same disclosure, 2026-06-06. Not maintained by BitoPro. |
| `bitopro-trade-guard` | Tombstoned (all versions unpublished). Previously abused; superseded by the scoped `@bitopro/trade-guard`. |
| `bitopro-ai-trade`, other `bitopro-*` | Unclaimed — reserve defensively; do not trust if published by anyone else. |

A real attacker publishing under these names could ship a malicious
`preinstall` / `postinstall` script that steals `BITOPRO_API_KEY` /
`BITOPRO_API_SECRET` or achieves host code execution on anyone who installs
them. **Do not install unscoped `bitopro-*` packages.**

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

- **2026-06** — Dependency-confusion exposure on unscoped skill package names
  (`bitopro-spot`, `bitopro-market-intel`); CWE-427 / CWE-829. Reported with a
  non-destructive proof-of-concept. _Researcher credit pending consent._

## Bug Bounty

We do not currently operate a formal paid bug bounty program for the skills hub.
Researchers reporting valid in-scope issues will be credited in this file (with
permission) and may receive small tokens of appreciation at our discretion.

The BitoPro exchange platform itself runs a separate bounty program — see
<https://www.bitopro.com/security> for details.
