---
name: bitopro-spot
description: >
  Full BitoPro exchange API wrapper for cryptocurrency trading.
  Use when: checking crypto prices on BitoPro, viewing order books, getting candlestick charts,
  checking account balances, placing buy/sell orders, cancelling orders, managing open orders,
  querying trade fills, batch order operations, viewing deposit/withdrawal history,
  initiating withdrawals, or looking up trading pair info, fees, and currency details.
  Supports TWD (New Taiwan Dollar) fiat trading pairs.
version: 2.0.0
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
homepage: https://github.com/bitoex/bitopro-skills-hub
license: MIT
---

# BitoPro Spot Skill

You are an AI agent equipped with the full BitoPro cryptocurrency exchange API (22 endpoints). Use this skill when the user needs to: check crypto prices, view order books, look up candlestick charts, query trading pair info and fees, get OTC prices, check account balances, place or batch-place orders, cancel single/batch/all orders, query order details and trade fills, or view deposit and withdrawal history on BitoPro. BitoPro is a Taiwan-based exchange that supports TWD (New Taiwan Dollar) fiat trading pairs.

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
| `/provisioning/trading-pairs` | GET | Trading pair info | No |
| `/provisioning/currencies` | GET | Currency info | No |
| `/provisioning/limitations-and-fees` | GET | Fees and limits | No |
| `/price/otc/{currency}` | GET | OTC buy/sell price | No |
| `/accounts/balance` | GET | Account balances | Yes |
| `/orders/{pair}` | POST | Create order | Yes |
| `/orders/batch` | POST | Create batch orders (max 10) | Yes |
| `/orders/{pair}/{orderId}` | GET | Get single order | Yes |
| `/orders/{pair}/{orderId}` | DELETE | Cancel order | Yes |
| `/orders` | PUT | Cancel batch orders | Yes |
| `/orders/all` or `/orders/{pair}` | DELETE | Cancel all orders | Yes |
| `/orders/open` | GET | Open orders | Yes |
| `/orders/all/{pair}` | GET | Order history | Yes |
| `/orders/trades/{pair}` | GET | Trade fills | Yes |
| `/wallet/depositHistory/{currency}` | GET | Deposit history | Yes |
| `/wallet/withdrawHistory/{currency}` | GET | Withdraw history | Yes |
| `/wallet/withdraw/{currency}/{serial}` | GET | Get withdraw detail | Yes |
| `/wallet/withdraw/{currency}` | POST | Create withdraw | Yes |

## Enums

**Order Side:** `BUY`, `SELL` | **Order Type:** `LIMIT`, `MARKET`, `STOP_LIMIT` | **Time in Force:** `GTC` (default), `POST_ONLY`

**Status Kind Filter:** `OPEN`, `DONE`, `ALL`

**Order Status Codes:** -1 (Not Triggered), 0 (Unfilled), 1 (Partial Fill), 2 (Completed), 3 (Partial Complete + Cancelled), 4 (Cancelled), 6 (Post-Only Cancelled)

**Candlestick Resolution:** `1m`, `5m`, `15m`, `30m`, `1h`, `3h`, `4h`, `6h`, `12h`, `1d`, `1w`, `1M`

**Deposit Status (crypto):** `PROCESSING`, `COMPLETE`, `EXPIRED`, `INVALID`, `WAIT_PROCESS`, `CANCELLED`

**Deposit Status (TWD):** `PROCESSING`, `COMPLETE`, `INVALID`, `WAIT_PROCESS`, `CANCELLED`, `FAILED`

**Withdraw Status (crypto):** `PROCESSING`, `COMPLETE`, `EXPIRED`, `INVALID`, `WAIT_PROCESS`, `WAIT_CONFIRMATION`, `EMAIL_VERIFICATION`, `CANCELLED`

**Withdraw Status (TWD):** `PROCESSING`, `COMPLETE`, `INVALID`, `WAIT_PROCESS`, `EMAIL_VERIFICATION`, `CANCELLED`, `FAILED`

**Withdraw Protocol:** `MAIN`, `ERC20`, `OMNI`, `TRX`, `BSC`, `POLYGON`

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

### Tool 10: `get_trading_pairs`

- **endpoint:** `GET /provisioning/trading-pairs` | **auth:** false
- **params:** none
- **returns:** `data[]` with `pair`, `base`, `quote`, `basePrecision`, `quotePrecision`, `minLimitBaseAmount`, `maxLimitBaseAmount`, `minMarketBuyQuoteAmount`, `orderOpenLimit`, `maintain`, `amountPrecision`

### Tool 11: `get_currencies`

- **endpoint:** `GET /provisioning/currencies` | **auth:** false
- **params:** none
- **returns:** `data[]` with `currency`, `withdrawFee`, `minWithdraw`, `maxWithdraw`, `maxDailyWithdraw`, `withdraw` (bool), `deposit` (bool), `depositConfirmation`

### Tool 12: `get_limitations_and_fees`

- **endpoint:** `GET /provisioning/limitations-and-fees` | **auth:** false
- **params:** none
- **returns:** `tradingFeeRate[]` (VIP tiers with maker/taker fees), `restrictionsOfWithdrawalFees[]`, `cryptocurrencyDepositFeeAndConfirmation[]`, `ttCheckFeesAndLimitationsLevel1[]`, `ttCheckFeesAndLimitationsLevel2[]`

### Tool 13: `get_otc_price`

- **endpoint:** `GET /price/otc/{currency}` | **auth:** false
- **params:** `currency` (required, e.g. `btc`)
- **returns:** `currency`, `buySwapQuotation.twd.exchangeRate`, `sellSwapQuotation.twd.exchangeRate`

### Tool 14: `create_batch_orders`

- **endpoint:** `POST /orders/batch` | **auth:** true | **rate_limit:** 90 req/min
- **signing:** `{ ...requestBody, "nonce": timestamp_ms }` (no `identity`)
- **params:** Array of up to 10 order objects, each with: `pair` (required), `action` (BUY/SELL), `type` (LIMIT/MARKET), `amount` (required), `price` (required for LIMIT), `timestamp` (ms), `timeInForce`, `clientId`
- **safety:** Always confirm all order details with user before executing.

### Tool 15: `cancel_batch_orders`

- **endpoint:** `PUT /orders` | **auth:** true | **rate_limit:** 2 req/sec
- **signing:** `{ ...requestBody, "nonce": timestamp_ms }` (no `identity`)
- **params:** JSON object keyed by pair, values are arrays of order IDs. e.g. `{ "BTC_USDT": ["123", "456"], "ETH_USDT": ["789"] }`
- **safety:** Always confirm cancellation targets with user before executing.

### Tool 16: `cancel_all_orders`

- **endpoint:** `DELETE /orders/all` or `DELETE /orders/{pair}` | **auth:** true | **rate_limit:** 1 req/sec
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `pair` (optional — omit to cancel all pairs)
- **safety:** Always confirm with user before executing. This cancels ALL open orders.

### Tool 17: `get_order`

- **endpoint:** `GET /orders/{pair}/{orderId}` | **auth:** true
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `pair` (required), `orderId` (required)
- **returns:** Full order object with `id`, `pair`, `price`, `avgExecutionPrice`, `action`, `type`, `status`, `originalAmount`, `remainingAmount`, `executedAmount`, `fee`, `feeSymbol`, `bitoFee`, `stopPrice`, `condition`, `timeInForce`, `createdTimestamp`, `updatedTimestamp`
- **note:** History available only for past 90 days.

### Tool 18: `get_trades`

- **endpoint:** `GET /orders/trades/{pair}` | **auth:** true
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `pair` (required), `startTimestamp` (ms, default 90d ago), `endTimestamp` (ms, default now), `orderId` (filter by order), `tradeId` (pagination cursor), `limit` (1-1000, default 100)
- **returns:** `data[]` with `tradeId`, `orderId`, `price`, `action`, `baseAmount`, `quoteAmount`, `fee`, `feeSymbol`, `isTaker`, `createdTimestamp`

### Tool 19: `get_deposit_history`

- **endpoint:** `GET /wallet/depositHistory/{currency}` | **auth:** true
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `currency` (required), `startTimestamp` (ms), `endTimestamp` (ms), `limit` (1-100, default 20), `id` (pagination cursor), `statuses` (comma-separated), `txID` (crypto only)
- **returns:** `data[]` with `serial`, `timestamp`, `address`, `amount`, `fee`, `total`, `status`, `txid`, `protocol`, `id`
- **note:** Max query window 90 days. `txID` filter not supported for TWD.

### Tool 20: `get_withdraw_history`

- **endpoint:** `GET /wallet/withdrawHistory/{currency}` | **auth:** true
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `currency` (required), `startTimestamp` (ms), `endTimestamp` (ms), `limit` (1-100, default 20), `id` (pagination cursor), `statuses` (comma-separated), `txID` (crypto only)
- **returns:** `data[]` with `serial`, `timestamp`, `address`, `amount`, `fee`, `total`, `status`, `txid`, `protocol`, `id`
- **note:** Max query window 90 days. `txID` filter not supported for TWD.

### Tool 21: `get_withdraw`

- **endpoint:** `GET /wallet/withdraw/{currency}/{serial}` or `GET /wallet/withdraw/{currency}/id/{id}` | **auth:** true
- **signing:** `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **params:** `currency` (required), `serial` or `id` (required — use one to look up)
- **returns:** `serial`, `protocol`, `address`, `amount`, `fee`, `total`, `status`, `id`, `timestamp`

### Tool 22: `create_withdraw`

- **endpoint:** `POST /wallet/withdraw/{currency}` | **auth:** true | **rate_limit:** 60 req/min
- **signing:** `{ ...requestBody, "nonce": timestamp_ms }` (no `identity`)
- **params:** `currency` (path, required — currency name without protocol), `amount` (required), `protocol` (default `MAIN`; options: `ERC20`, `TRX`, `BSC`, `POLYGON`), `address` (required for non-TWD), `message` (required for EOS/BNB), `bankAccountSerial` (TWD only), `bankSerial` (TWD only)
- **returns:** `serial`, `currency`, `protocol`, `address`, `amount`, `fee`, `total`, `id`
- **critical:** Withdraw addresses must be pre-configured at https://www.bitopro.com/address
- **safety:** Always confirm withdrawal details with user before executing. Display amount, address, fee, and network.

## Agent Behavior

1. **Validate trading pair format** — must be `{base}_{quote}` lowercase with underscore.
2. **Handle errors gracefully.** Explain API errors to the user and suggest corrections.
3. **Respect rate limits.** Public: 600 req/min/IP. Private: 600 req/min/IP + 600 req/min/UID. Create: 1200/min. Batch create: 90/min. Cancel: 900/min. Cancel all/batch: 1-2/sec. Open orders: 5/sec. Withdraw: 60/min.
4. **Market order specifics.** For MARKET BUY, `amount` is in **quote currency** (TWD), not base.
5. **Candlestick timestamps.** Query `from`/`to` in **seconds**, response `timestamp` in **milliseconds**.
6. **Withdrawal safety.** Always display amount, destination address, fee, and network/protocol for user confirmation before executing `create_withdraw`. Withdraw addresses must be pre-configured on the BitoPro website.
7. **Batch operations.** Batch create supports max 10 orders. Always show the full list of orders/cancellations for user confirmation.

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
User-Agent: bitopro-spot/2.0.0 (Skill)
X-Execution-Source: Claude-Skill
X-Skill-Name: bitopro/spot
X-Skill-Version: 2.0.0
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
