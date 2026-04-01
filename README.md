# BitoPro Skills Hub

An open skills marketplace that gives AI agents native access to cryptocurrency trading on [BitoPro](https://www.bitopro.com/) — Taiwan's leading crypto exchange with TWD (New Taiwan Dollar) fiat trading pairs.

Built for [ClawHub](https://clawhub.ai/) and compatible with Claude Code / OpenClaw skill ecosystems.

## Available Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [bitopro-spot](./skills/bitopro/spot/) | Full spot exchange API wrapper — tickers, order book, trades, candlesticks, balances, order CRUD (9 endpoints) | Published |
| bitopro-ai-trade | NLP-powered trading assistant — parses Chinese/English natural language into market orders with 10K TWD safety limit | Coming soon |

## Quick Start

### Install via ClawHub

```bash
npx clawhub install bitopro-spot
```

### Manual Installation

Clone and point your agent to the skill directory:

```bash
git clone https://github.com/bitoadam/bitopro-skills-hub.git
```

### Configuration

Set the following environment variables (required for private endpoints):

```bash
export BITOPRO_API_KEY="your_api_key"
export BITOPRO_API_SECRET="your_api_secret"
export BITOPRO_EMAIL="your_registered_email"
```

> API credentials can be generated from [BitoPro Dashboard → API Management](https://www.bitopro.com/api).

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

## License

[MIT](./LICENSE)
