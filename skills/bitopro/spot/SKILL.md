---
name: bitopro-spot
description: >
  Full BitoPro spot exchange API wrapper for cryptocurrency trading.
  Use when: checking crypto prices on BitoPro, viewing order books, getting candlestick charts,
  checking account balances, placing buy/sell orders, cancelling orders, or managing open orders.
  Supports TWD (New Taiwan Dollar) fiat trading pairs.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - BITOPRO_API_KEY
        - BITOPRO_API_SECRET
        - BITOPRO_EMAIL
    primaryEnv: BITOPRO_API_KEY
    env:
      - name: BITOPRO_API_KEY
        description: "API Key from BitoPro dashboard"
        required: true
        sensitive: true
      - name: BITOPRO_API_SECRET
        description: "API Secret for HMAC-SHA384 signing"
        required: true
        sensitive: true
      - name: BITOPRO_EMAIL
        description: "BitoPro registered email (used as identity in GET/DELETE payloads)"
        required: true
        sensitive: false
category: crypto-trading
emoji: "📈"
homepage: https://github.com/bitoadam/bitopro-skills-hub
license: MIT
---

# BitoPro Spot Skill

You are an AI agent equipped with the BitoPro cryptocurrency exchange API. Use this skill when the user needs to check crypto prices, view order books, look up candlestick charts, check account balances, place buy/sell orders, cancel orders, or manage open orders on BitoPro. BitoPro is a Taiwan-based exchange that supports TWD (New Taiwan Dollar) fiat trading pairs.

## Quick Start

1. Set environment variables: `BITOPRO_API_KEY`, `BITOPRO_API_SECRET`, `BITOPRO_EMAIL`
2. Public endpoints (tickers, order book, trades, candlesticks) require no auth
3. Private endpoints (balance, orders) require HMAC-SHA384 signing — see [references/authentication.md](./references/authentication.md)

## Prerequisites

| Requirement | Details |
|-------------|---------|
| API credentials | BitoPro dashboard → API Management |
| Environment variables | `BITOPRO_API_KEY`, `BITOPRO_API_SECRET`, `BITOPRO_EMAIL` |
| Base URL | `https://api.bitopro.com/v3` |
| Pair format | Lowercase with underscore: `btc_twd`, `eth_twd`, `usdt_twd` |

## Security Notes

- `BITOPRO_API_KEY`: Show first 5 + last 4 characters only (e.g., `abc12...6789`)
- `BITOPRO_API_SECRET`: Always mask, never display any portion
- Before placing or cancelling any order, **display full order details and obtain explicit user confirmation**
- All Skill orders must include `clientId: 2147483647` for tracking

## Quick Reference

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/tickers/{pair}` | GET | Real-time ticker data | No |
| `/order-book/{pair}` | GET | Order book depth | No |
| `/trades/{pair}` | GET | Recent trade records | No |
| `/trading-history/{pair}` | GET | OHLCV candlesticks | No |
| `/accounts/balance` | GET | Account balances | Yes |
| `/orders/{pair}` | POST | Create order | Yes |
| `/orders/{pair}/{orderId}` | DELETE | Cancel order | Yes |
| `/orders/open` | GET | Open orders | Yes |
| `/orders/all/{pair}` | GET | Order history | Yes |

## Enums

**Order Side:** `BUY`, `SELL` | **Order Type:** `LIMIT`, `MARKET`, `STOP_LIMIT` | **Time in Force:** `GTC` (default), `POST_ONLY`

**Status Kind Filter:** `OPEN`, `DONE`, `ALL`

**Order Status Codes:** -1 (Not Triggered), 0 (Unfilled), 1 (Partial Fill), 2 (Completed), 3 (Partial Complete + Cancelled), 4 (Cancelled), 6 (Post-Only Cancelled)

**Candlestick Resolution:** `1m`, `5m`, `15m`, `30m`, `1h`, `3h`, `4h`, `6h`, `12h`, `1d`, `1w`, `1M`

## Authentication

Private endpoints require HMAC-SHA384 signing. Headers: `X-BITOPRO-APIKEY`, `X-BITOPRO-PAYLOAD`, `X-BITOPRO-SIGNATURE`.

| Method | Payload Source |
|--------|----------------|
| GET / DELETE | `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }` |
| POST / PUT | `{ ...requestBody, "nonce": timestamp_ms }` (**no `identity`**) |

> Full signing guide with Python/Go examples: [references/authentication.md](./references/authentication.md)

## Tools

### Tool 1: `get_tickers`

- **endpoint:** `GET /tickers/{pair}` | **auth:** false
- **params:** `pair` (string, optional) — e.g. `btc_twd`. Omit for all pairs.
- **returns:** `lastPrice`, `high24hr`, `low24hr`, `volume24hr`, `priceChange24hr`, `isBuyer`

### Tool 2: `get_order_book`

- **endpoint:** `GET /order-book/{pair}` | **auth:** false
- **params:** `pair` (string, required), `limit` (int, optional: 1/5/10/20/30/50, default 5), `scale` (int, optional)
- **returns:** `asks[]` and `bids[]` with `price`, `amount`, `count`, `total`

### Tool 3: `get_trades`

- **endpoint:** `GET /trades/{pair}` | **auth:** false
- **params:** `pair` (string, required)
- **returns:** `data[]` with `price`, `amount`, `isBuyer`, `timestamp`

### Tool 4: `get_candlesticks`

- **endpoint:** `GET /trading-history/{pair}` | **auth:** false
- **params:** `pair` (required), `resolution` (required), `from` (required, Unix seconds), `to` (required, Unix seconds)
- **returns:** `data[]` with `timestamp` (ms!), `open`, `high`, `low`, `close`, `volume`
- **note:** `1m`/`5m` only last 365 days. Query params in **seconds**, response timestamp in **milliseconds**.

### Tool 5: `get_account_balance`

- **endpoint:** `GET /accounts/balance` | **auth:** true
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** none
- **returns:** `data[]` with `currency`, `amount`, `available`, `stake`, `tradable`

### Tool 6: `create_order`

- **endpoint:** `POST /orders/{pair}` | **auth:** true
- **signing:** `{ ...requestBody, "nonce": timestamp_ms }` (no `identity`)
- **params:** `pair` (required), `action` (BUY/SELL, required), `type` (LIMIT/MARKET/STOP_LIMIT, required), `amount` (required), `timestamp` (required), `price` (required for LIMIT/STOP_LIMIT), `stopPrice`, `condition` (>=, <=), `timeInForce`, `clientId` (default: 2147483647)
- **critical:** `nonce` must be in both signing payload AND request body. For MARKET BUY, `amount` is in quote currency (TWD).
- **safety:** Always confirm order details with user before executing.

### Tool 7: `cancel_order`

- **endpoint:** `DELETE /orders/{pair}/{orderId}` | **auth:** true
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `pair` (required), `orderId` (required)

### Tool 8: `get_open_orders`

- **endpoint:** `GET /orders/open` | **auth:** true | **rate_limit:** 5 req/sec
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `pair` (optional, filter)
- **returns:** Order objects with `id`, `pair`, `action`, `type`, `price`, `originalAmount`, `remainingAmount`, `executedAmount`, `avgExecutionPrice`, `status`, `fee`, `feeSymbol`, `timeInForce`, `createdTimestamp`, `updatedTimestamp`

### Tool 9: `get_order_history`

- **endpoint:** `GET /orders/all/{pair}` | **auth:** true
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `pair` (required), `startTimestamp` (ms, default 90d ago), `endTimestamp` (ms, default now), `statusKind` (OPEN/DONE/ALL), `status` (code), `orderId` (pagination cursor), `limit` (1-1000, default 100)

## Agent Behavior

1. **Validate trading pair format** — must be `{base}_{quote}` lowercase with underscore.
2. **Handle errors gracefully.** Explain API errors to the user and suggest corrections.
3. **Respect rate limits.** Public: 600 req/min/IP. Private: 600 req/min/IP + 600 req/min/UID. Create: 1200/min. Cancel: 900/min. Open orders: 5/sec.
4. **Market order specifics.** For MARKET BUY, `amount` is in **quote currency** (TWD), not base.
5. **Candlestick timestamps.** Query `from`/`to` in **seconds**, response `timestamp` in **milliseconds**.

## Error Handling

| HTTP Code | Description |
|-----------|-------------|
| 400 | Bad Request (invalid parameters) |
| 401 | Unauthorized (invalid API key or signature) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found (invalid pair or order ID) |
| 429 | Rate Limit Exceeded |

## Skill Identification

All requests must include these headers for tracking:

```
User-Agent: bitopro-spot/1.0.0 (Skill)
X-Execution-Source: Claude-Skill
X-Skill-Name: bitopro/spot
X-Skill-Version: 1.0.0
X-Client-Type: AI-Agent
```

All order requests must include `clientId: 2147483647` to distinguish AI-executed orders from manual trades.

## File Reference

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill definition (this file) |
| `references/authentication.md` | Full HMAC-SHA384 signing guide with Python/Go examples |
| `references/endpoints.md` | Detailed endpoint specs with full request/response examples |
| `evals/evals.json` | Evaluation test cases for skill verification |
| `LICENSE.md` | MIT license |
