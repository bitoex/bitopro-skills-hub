# BitoPro Skills Hub

An open skills marketplace that gives AI agents native access to cryptocurrency trading on [BitoPro](https://www.bitopro.com/) — Taiwan's leading crypto exchange with TWD (New Taiwan Dollar) fiat trading pairs.

Built for [ClawHub](https://clawhub.ai/) and compatible with Claude Code / OpenClaw skill ecosystems.

## Available Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [bitopro-spot](./skills/bitopro/spot/) | Full exchange API wrapper — tickers, order book, trades, candlesticks, trading pairs, fees, OTC price, balances, order CRUD, batch orders, trade fills, deposit/withdraw history (22 endpoints) | Published |
| [bitopro-market-intel](./skills/bitopro/market-intel/) | Crypto market intelligence scoped to BitoPro spot coins — Fear & Greed index, BTC/ETH-dominance macro overview, BitoPro coin rankings, BitoPro coins on trending list, company BTC/ETH holdings, multi-timeframe coin details (7 tools, free APIs) | Published |

## Quick Start

> ⚠️ **Security notice (2026-06):** third parties have published unofficial
> packages/skills under our names on **ClawHub** (`bitopro-spot`) and on **npm**
> (`bitopro-spot`, `bitopro-market-intel`). **Until we reclaim those names,
> install only by cloning this repository.** Do **not** run
> `npx clawhub install bitopro-spot` or `npm i bitopro-*` — they currently
> resolve to third-party content. See [SECURITY.md](./SECURITY.md).

### Install (clone this repository)

```bash
git clone https://github.com/bitoex/bitopro-skills-hub.git
```

Then point your agent at the skill directory, e.g. `skills/bitopro/spot/`.

### Configuration

Set the following environment variables (required for private endpoints):

```bash
export BITOPRO_API_KEY="your_api_key"
export BITOPRO_API_SECRET="your_api_secret"
export BITOPRO_EMAIL="your_registered_email"
```

> API credentials can be generated from [BitoPro Dashboard → API Management](https://www.bitopro.com/api).

Run private endpoints only in a trusted, patched agent runtime. Do not export
`BITOPRO_API_KEY`, `BITOPRO_API_SECRET`, or `BITOPRO_EMAIL` into an agent
gateway until its runtime administration, external tool configuration, hook
installation, and hook context controls have been reviewed. If runtime patch
status cannot be verified, use public-only mode. If the runtime is trusted but
hook provenance cannot be verified, require explicit confirmation for every
private action.

## Skill Structure

Each skill follows the [ClawHub standard](https://clawhub.ai/tdavis009/clawhub-skill-guide):

```
skills/bitopro/<skill-name>/
├── SKILL.md              # Core skill definition (< 500 lines)
├── references/           # Detailed docs loaded on demand
│   ├── authentication.md # HMAC-SHA384 signing guide (Python/Go)
│   └── endpoints.md      # Full endpoint specs with examples
├── evals/
│   └── evals.json        # Evaluation test cases
└── LICENSE.md            # MIT license
```

## Skill Identification

All skills share a unified identification mechanism for tracking AI-initiated orders:

- **HTTP Headers:** `X-Execution-Source: Claude-Skill`, `X-Skill-Name`, `X-Client-Type: AI-Agent`
- **Order ClientId:** `2147483647` — reserved identifier for all skill-originated orders

This allows users and operators to distinguish AI-executed trades from manual ones in analytics and monitoring.

## Security

- API secrets are never displayed in agent output
- All order operations require explicit user confirmation before execution
- Sensitive environment variables are declared in SKILL.md frontmatter with `sensitive: true`
- Session-aware fast paths require a trusted runtime and a verified
  `bitopro-trade-guard` hook. Unknown hook source, unpinned npm install,
  or failed hook loading must fall back to explicit per-order confirmation.
  Unknown or unreviewed runtime security status must use public-only mode.
- **Supply chain:** install skills by `git clone` from this repo (the ClawHub
  and npm names for the skills have been squatted by third parties as of
  2026-06). Verify the publisher is the `bitoex` npm account before installing
  any `bitopro-*` / `@bito*` package. See [SECURITY.md](./SECURITY.md) for the
  current list of official vs squatted names and how to report a vulnerability.

## License

[MIT](./LICENSE)
