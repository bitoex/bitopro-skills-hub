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
| Critical | Trading API key leak, order execution bypass, high-impact supply-chain compromise | 24 hours |
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
  Claude Code) — please report to the respective platform. Runtime security or
  tool-loading issues in those platforms are not code defects in this
  repository, but they are security-relevant for any deployment that injects
  BitoPro API credentials into that runtime.
- Social engineering against BitoPro staff
- Denial-of-service against BitoPro infrastructure
- Issues in transitive dev dependencies that don't impact skill security posture
- Unverified theoretical attacks without enough detail to reproduce

## Distribution Notice (Important)

Install these skills by **cloning this repository** and pointing your agent at
`skills/bitopro/<skill-name>/`:

```bash
git clone https://github.com/bitoex/bitopro-skills-hub.git
```

The skills (`bitopro-spot`, `bitopro-market-intel`) are **NOT** published to
the public npm registry. As of 2026-06, third parties have also claimed the
ClawHub slug `bitopro-spot` and the unscoped npm names `bitopro-spot` /
`bitopro-market-intel`.

> ⚠️ **Until those names are reclaimed, do not run
> `npx clawhub install bitopro-spot` or `npm i bitopro-*`** — they resolve to
> third-party content. Install via `git clone` from this repository.

### Our official npm packages

BitoPro publishes npm packages from the `bitoex` account and related BitoPro
maintainer accounts. For scoped packages, verify both the package maintainers and
the scope/org ownership in npm before relying on the package in production. As
of 2026-06 our official npm packages include:

| Package | Scope | Role |
|---|---|---|
| `@bitopro/trade-guard` | scoped | trade-guard hook (this repo) |
| `@bitoex/ccxt` | scoped | BitoPro CCXT fork |
| `bitopro-api-node` | unscoped | official BitoPro Node.js SDK |

Before installing any `bitopro-*` / `@bito*` package, **verify the publisher is
the `bitoex` npm account.** Do not assume every unscoped `bitopro-*` name is
ours (it is not) — and do not assume every unscoped `bitopro-*` name is hostile
either (`bitopro-api-node` is genuinely ours). Verify the publisher.

### Known unofficial / squatted names

These names are published by third parties as of 2026-06 and are **not
maintained by BitoPro** — a dependency-confusion / slug-squatting exposure
(CWE-427 / CWE-829):

| Name | Channel | Status (2026-06) |
|---|---|---|
| `bitopro-spot` | **ClawHub** | Not controlled by BitoPro until reclaimed |
| `bitopro-spot` | npm (unscoped) | Not controlled by BitoPro until reclaimed |
| `bitopro-market-intel` | npm (unscoped) | Not controlled by BitoPro until reclaimed |
| `bitopro-trade-guard` | npm (unscoped) | Tombstoned; superseded by scoped `@bitopro/trade-guard` |
| `bitopro-ai-trade`, other `bitopro-*` | npm / ClawHub | Unclaimed — reserve defensively |

Content under uncontrolled names can expose credentials or execute untrusted
code. **Install skills only by `git clone` from this repository until the names
are reclaimed.**

## Runtime Platform Requirements

This repository contains skill definitions and the `bitopro-trade-guard` hook;
it does not contain the agent runtime, registry service, external tool launcher,
or platform policy engine. Findings in those components must be fixed in the
respective platform, but they affect BitoPro deployments when credentials are
present in the same process.

Before enabling private trading or account tools in an agent runtime, operators
must verify:

| Component | Required status before private trading |
|---|---|
| Skill installation | Untrusted skills are disabled or reviewed before use |
| Hook installation | Hook source, package owner, exact version, and integrity are verified |
| Runtime administration | Admin APIs are access-controlled, audited, and not exposed to untrusted clients |
| External tools | Command-spawning integrations are disabled unless explicitly trusted and isolated |

If any required status is unknown, do not place BitoPro API credentials in that
runtime. Use public-only tools, a local audited checkout, or a deployment wrapper
that enforces explicit confirmation on every private order and withdrawal.

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
