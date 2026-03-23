---
name: spot
description: Use when user needs to trade cryptocurrencies on BitoPro exchange, check market data, manage orders, or view account balances. Supports both public (market data) and private (trading) operations via BitoPro API. Covers 9 endpoints including tickers, order books, trades, candlesticks, balances, and order management.
metadata:
  version: 1.0.0
  author: bitopro-community
license: MIT
---

# BitoPro Spot Skill

You are an AI agent equipped with the BitoPro cryptocurrency exchange API. Use this skill when the user needs to check crypto prices, view order books, look up candlestick charts, check account balances, place buy/sell orders, cancel orders, or manage open orders on BitoPro. BitoPro is a Taiwan-based exchange that supports TWD (New Taiwan Dollar) fiat trading pairs.

## Quick Reference

| Endpoint | Method | Description | Required Params | Optional Params | Auth |
|----------|--------|-------------|-----------------|-----------------|------|
| `/tickers/{pair}` | GET | Real-time ticker data | None | pair | No |
| `/order-book/{pair}` | GET | Order book depth | pair | limit, scale | No |
| `/trades/{pair}` | GET | Recent trade records | pair | None | No |
| `/trading-history/{pair}` | GET | OHLCV candlesticks | pair, resolution, from, to | None | No |
| `/accounts/balance` | GET | Account balances | None | None | Yes |
| `/orders/{pair}` | POST | Create order | pair, action, type, amount, timestamp | price, stopPrice, condition, timeInForce, clientId | Yes |
| `/orders/{pair}/{orderId}` | DELETE | Cancel order | pair, orderId | None | Yes |
| `/orders/open` | GET | Open orders | None | pair | Yes |
| `/orders/all/{pair}` | GET | Order history | pair | startTimestamp, endTimestamp, statusKind, status, orderId, limit | Yes |

## Parameters

### Base URL

```
https://api.bitopro.com/v3
```

### Trading Pair Format

All trading pairs use **lowercase** with **underscore** separator:

```
btc_twd, eth_twd, usdt_twd, sol_twd, bito_eth, ...
```

### Enums

**Order Side:** `BUY`, `SELL`

**Order Type:** `LIMIT`, `MARKET`, `STOP_LIMIT`

**Time in Force:** `GTC` (default), `POST_ONLY`

**Status Kind Filter:** `OPEN`, `DONE`, `ALL`

**Order Status Codes:**

| Code | Status |
|------|--------|
| -1 | Not Triggered (stop-limit pending) |
| 0 | In Progress (unfilled) |
| 1 | In Progress (partially filled) |
| 2 | Completed (fully filled) |
| 3 | Completed (partially filled, then cancelled) |
| 4 | Cancelled |
| 6 | Post-Only Cancelled |

**Candlestick Resolution:** `1m`, `5m`, `15m`, `30m`, `1h`, `3h`, `4h`, `6h`, `12h`, `1d`, `1w`, `1M`

## Authentication

Private endpoints require three environment variables:

```
BITOPRO_API_KEY    — API Key (from BitoPro dashboard)
BITOPRO_API_SECRET — API Secret (used for HMAC signing)
BITOPRO_EMAIL      — BitoPro registered email (used as identity for GET/DELETE)
```

### Signing Algorithm

**Payload construction rules (differ by HTTP method):**

| Method | Payload Source |
|--------|----------------|
| GET / DELETE | `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }` |
| POST / PUT | `{ ...requestBody, "nonce": timestamp_ms }` (**no `identity`**) |

**Signing steps:**

1. Build payload object based on HTTP method (see table above)
2. `encoded_payload` = Base64Encode(JSON.stringify(payload_object))
3. `signature` = HMAC-SHA384(`encoded_payload`, `API_SECRET`).hexdigest()

**Header inclusion rules:**

| Header | GET | POST/PUT | DELETE |
|--------|-----|----------|--------|
| `X-BITOPRO-APIKEY` | Yes | Yes | Yes |
| `X-BITOPRO-PAYLOAD` | Yes | Yes | Yes |
| `X-BITOPRO-SIGNATURE` | Yes | Yes | Yes |

> All three headers are required for all authenticated requests, including DELETE.

### Python Signing Example

```python
import hmac, hashlib, base64, json, time

def build_headers(method: str, api_key: str, api_secret: str, email: str, body: dict = None) -> dict:
    nonce = int(time.time() * 1000)

    if method.upper() in ('GET', 'DELETE'):
        payload_obj = {"identity": email, "nonce": nonce}
    else:
        payload_obj = {**(body or {}), "nonce": nonce}

    payload = base64.b64encode(
        json.dumps(payload_obj).encode('utf-8')
    ).decode('utf-8')

    signature = hmac.new(
        api_secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha384
    ).hexdigest()

    headers = {
        'X-BITOPRO-APIKEY': api_key,
        'X-BITOPRO-PAYLOAD': payload,
        'X-BITOPRO-SIGNATURE': signature,
        'Content-Type': 'application/json',
    }

    return headers
```

> Full signing guide with Go examples: [references/authentication.md](./references/authentication.md)

---

## Tools

---

### Tool 1: `get_tickers`

- **name:** `get_tickers`
- **description:** Get real-time ticker data from BitoPro. Returns latest price, 24h high/low, volume, and price change for one or all trading pairs.
- **auth_required:** false
- **endpoint:** `GET /tickers/{pair}`

**parameters:**

```json
{
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "description": "Trading pair, e.g. btc_twd. Omit to return all pairs."
    }
  },
  "required": []
}
```

**example:**

```
GET https://api.bitopro.com/v3/tickers/btc_twd
```

```json
{
  "data": [
    {
      "pair": "btc_twd",
      "lastPrice": "2850000.00000000",
      "high24hr": "2890000.00000000",
      "low24hr": "2810000.00000000",
      "volume24hr": "156.78901234",
      "priceChange24hr": "1.42",
      "isBuyer": true
    }
  ]
}
```

---

### Tool 2: `get_order_book`

- **name:** `get_order_book`
- **description:** Get the order book depth (bid/ask levels) for a specific trading pair.
- **auth_required:** false
- **endpoint:** `GET /order-book/{pair}`

**parameters:**

```json
{
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "description": "Trading pair, e.g. btc_twd"
    },
    "limit": {
      "type": "integer",
      "description": "Number of depth levels",
      "enum": [1, 5, 10, 20, 30, 50],
      "default": 5
    },
    "scale": {
      "type": "integer",
      "description": "Price aggregation precision (varies by pair)",
      "default": 0
    }
  },
  "required": ["pair"]
}
```

**example:**

```
GET https://api.bitopro.com/v3/order-book/btc_twd?limit=5
```

```json
{
  "asks": [
    { "price": "2851000", "amount": "0.12", "count": 3, "total": "0.12" },
    { "price": "2852000", "amount": "0.35", "count": 2, "total": "0.47" }
  ],
  "bids": [
    { "price": "2849000", "amount": "0.08", "count": 1, "total": "0.08" },
    { "price": "2848000", "amount": "0.55", "count": 4, "total": "0.63" }
  ]
}
```

---

### Tool 3: `get_trades`

- **name:** `get_trades`
- **description:** Get the most recent trade records for a trading pair.
- **auth_required:** false
- **endpoint:** `GET /trades/{pair}`

**parameters:**

```json
{
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "description": "Trading pair, e.g. btc_twd"
    }
  },
  "required": ["pair"]
}
```

**example:**

```
GET https://api.bitopro.com/v3/trades/btc_twd
```

```json
{
  "data": [
    {
      "price": "2850000.00000000",
      "amount": "0.01200000",
      "isBuyer": false,
      "timestamp": 1696000000
    },
    {
      "price": "2849500.00000000",
      "amount": "0.00500000",
      "isBuyer": true,
      "timestamp": 1695999950
    }
  ]
}
```

---

### Tool 4: `get_candlesticks`

- **name:** `get_candlesticks`
- **description:** Get OHLCV candlestick data for a trading pair. Supports multiple time resolutions from 1 minute to 1 month.
- **auth_required:** false
- **endpoint:** `GET /trading-history/{pair}`

**parameters:**

```json
{
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "description": "Trading pair, e.g. btc_twd"
    },
    "resolution": {
      "type": "string",
      "description": "Candlestick time interval",
      "enum": ["1m", "5m", "15m", "30m", "1h", "3h", "4h", "6h", "12h", "1d", "1w", "1M"]
    },
    "from": {
      "type": "integer",
      "description": "Start time (Unix timestamp in seconds)"
    },
    "to": {
      "type": "integer",
      "description": "End time (Unix timestamp in seconds)"
    }
  },
  "required": ["pair", "resolution", "from", "to"]
}
```

> Note: `1m` and `5m` resolutions only provide data for the last 365 days. Response `timestamp` is in **milliseconds**.

**example:**

```
GET https://api.bitopro.com/v3/trading-history/btc_twd?resolution=1h&from=1695900000&to=1696000000
```

```json
{
  "data": [
    {
      "timestamp": 1695902400000,
      "open": "2840000",
      "high": "2855000",
      "low": "2835000",
      "close": "2850000",
      "volume": "12.34567890"
    }
  ]
}
```

---

### Tool 5: `get_account_balance`

- **name:** `get_account_balance`
- **description:** Get the user's account balances for all currencies on BitoPro, including total, available, and staked amounts.
- **auth_required:** true
- **endpoint:** `GET /accounts/balance`
- **signing:** Payload = `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`

**parameters:**

```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

**example:**

```
GET https://api.bitopro.com/v3/accounts/balance

Headers:
  X-BITOPRO-APIKEY: <api_key>
  X-BITOPRO-PAYLOAD: <base64_encoded_payload>
  X-BITOPRO-SIGNATURE: <hmac_sha384_hex>
```

```json
{
  "data": [
    { "currency": "twd", "amount": "100000", "available": "85000", "stake": "0", "tradable": true },
    { "currency": "btc", "amount": "0.5", "available": "0.3", "stake": "0.2", "tradable": true },
    { "currency": "eth", "amount": "5.0", "available": "5.0", "stake": "0", "tradable": true }
  ]
}
```

---

### Tool 6: `create_order`

- **name:** `create_order`
- **description:** Place a new buy or sell order on BitoPro. Supports LIMIT, MARKET, and STOP_LIMIT order types.
- **auth_required:** true
- **endpoint:** `POST /orders/{pair}`
- **signing:** Payload = `{ ...requestBody, "nonce": timestamp_ms }` (**no `identity`**)

**parameters:**

```json
{
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "description": "Trading pair, e.g. btc_twd"
    },
    "action": {
      "type": "string",
      "enum": ["BUY", "SELL"],
      "description": "Order side: buy or sell"
    },
    "type": {
      "type": "string",
      "enum": ["LIMIT", "MARKET", "STOP_LIMIT"],
      "description": "Order type"
    },
    "price": {
      "type": "string",
      "description": "Order price. Required for LIMIT and STOP_LIMIT. Not required for MARKET."
    },
    "amount": {
      "type": "string",
      "description": "Order quantity. For market BUY, this is the quote currency amount (e.g. TWD)."
    },
    "timestamp": {
      "type": "integer",
      "description": "Current timestamp in milliseconds"
    },
    "stopPrice": {
      "type": "string",
      "description": "Trigger price (only for STOP_LIMIT)"
    },
    "condition": {
      "type": "string",
      "enum": [">=", "<="],
      "description": "Trigger condition (only for STOP_LIMIT)"
    },
    "timeInForce": {
      "type": "string",
      "enum": ["GTC", "POST_ONLY"],
      "description": "Time in force. Default: GTC"
    },
    "clientId": {
      "type": "integer",
      "description": "Custom order ID (1–2147483647)"
    }
  },
  "required": ["pair", "action", "type", "amount", "timestamp"]
}
```

**example:**

```
POST https://api.bitopro.com/v3/orders/btc_twd

Headers:
  X-BITOPRO-APIKEY: <api_key>
  X-BITOPRO-PAYLOAD: <base64_encoded_payload>     <- included for POST
  X-BITOPRO-SIGNATURE: <hmac_sha384_hex>

Body:
{
  "action": "BUY",
  "amount": "0.001",
  "price": "2800000",
  "type": "LIMIT",
  "timestamp": 1696000000000,
  "nonce": 1696000000000
}
```

Signing payload and request body must both contain `nonce` (note: **no `identity`**):
```json
{
  "action": "BUY",
  "amount": "0.001",
  "price": "2800000",
  "type": "LIMIT",
  "timestamp": 1696000000000,
  "nonce": 1696000000000
}
```

Response:
```json
{
  "orderId": 1234567890,
  "action": "BUY",
  "amount": "0.001",
  "price": "2800000",
  "timestamp": 1696000000000,
  "timeInForce": "GTC"
}
```

> **Critical: The `nonce` field must be included in both the signing payload AND the HTTP request body. The API validates that the decoded payload matches the body. Omitting `nonce` from the body causes "Invalid payload" errors.**

> **Safety: Always confirm order details (pair, side, type, price, amount) with the user and obtain explicit approval before executing.**

---

### Tool 7: `cancel_order`

- **name:** `cancel_order`
- **description:** Cancel an existing order on BitoPro by order ID.
- **auth_required:** true
- **endpoint:** `DELETE /orders/{pair}/{orderId}`
- **signing:** Payload = `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **headers:** `X-BITOPRO-APIKEY` + `X-BITOPRO-PAYLOAD` + `X-BITOPRO-SIGNATURE`

**parameters:**

```json
{
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "description": "Trading pair, e.g. btc_twd"
    },
    "orderId": {
      "type": "string",
      "description": "The order ID to cancel"
    }
  },
  "required": ["pair", "orderId"]
}
```

**example:**

```
DELETE https://api.bitopro.com/v3/orders/btc_twd/1234567890

Headers:
  X-BITOPRO-APIKEY: <api_key>
  X-BITOPRO-PAYLOAD: <base64_encoded_payload>
  X-BITOPRO-SIGNATURE: <hmac_sha384_hex>
```

```json
{
  "action": "BUY",
  "amount": "0.001",
  "orderId": "1234567890",
  "price": "2800000",
  "timestamp": 1696000000000
}
```

---

### Tool 8: `get_open_orders`

- **name:** `get_open_orders`
- **description:** Get all open (unfilled or partially filled) orders for the user.
- **auth_required:** true
- **endpoint:** `GET /orders/open`
- **signing:** Payload = `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`
- **rate_limit:** 5 requests / second

**parameters:**

```json
{
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "description": "Filter by trading pair (e.g. btc_twd). Omit to return all pairs."
    }
  },
  "required": []
}
```

**example:**

```
GET https://api.bitopro.com/v3/orders/open?pair=btc_twd

Headers:
  X-BITOPRO-APIKEY: <api_key>
  X-BITOPRO-PAYLOAD: <base64_encoded_payload>
  X-BITOPRO-SIGNATURE: <hmac_sha384_hex>
```

```json
{
  "data": [
    {
      "id": "1234567890",
      "pair": "btc_twd",
      "action": "BUY",
      "type": "LIMIT",
      "price": "2800000",
      "originalAmount": "0.001",
      "remainingAmount": "0.001",
      "executedAmount": "0",
      "avgExecutionPrice": "0",
      "status": 0,
      "fee": "0",
      "feeSymbol": "btc",
      "bitoFee": "0",
      "timeInForce": "GTC",
      "createdTimestamp": 1696000000000,
      "updatedTimestamp": 1696000000000
    }
  ]
}
```

---

### Tool 9: `get_order_history`

- **name:** `get_order_history`
- **description:** Get historical order records. Supports filtering by status, time range, and pagination.
- **auth_required:** true
- **endpoint:** `GET /orders/all/{pair}`
- **signing:** Payload = `{ "identity": BITOPRO_EMAIL, "nonce": timestamp_ms }`

**parameters:**

```json
{
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "description": "Trading pair, e.g. btc_twd"
    },
    "startTimestamp": {
      "type": "integer",
      "description": "Start time (milliseconds). Default: 90 days ago"
    },
    "endTimestamp": {
      "type": "integer",
      "description": "End time (milliseconds). Default: now"
    },
    "statusKind": {
      "type": "string",
      "enum": ["OPEN", "DONE", "ALL"],
      "description": "Status category filter. Default: ALL"
    },
    "status": {
      "type": "integer",
      "description": "Specific status code: -1(not triggered), 0(in progress), 1(partial fill), 2(completed), 3(partial complete), 4(cancelled), 6(post-only cancelled)"
    },
    "orderId": {
      "type": "string",
      "description": "Pagination cursor (returns orders with id <= this value)"
    },
    "limit": {
      "type": "integer",
      "description": "Results per page (1–1000). Default: 100"
    }
  },
  "required": ["pair"]
}
```

**example:**

```
GET https://api.bitopro.com/v3/orders/all/btc_twd?statusKind=DONE&limit=10

Headers:
  X-BITOPRO-APIKEY: <api_key>
  X-BITOPRO-PAYLOAD: <base64_encoded_payload>
  X-BITOPRO-SIGNATURE: <hmac_sha384_hex>
```

```json
{
  "data": [
    {
      "id": "1234567890",
      "pair": "btc_twd",
      "action": "BUY",
      "type": "LIMIT",
      "price": "2800000",
      "originalAmount": "0.001",
      "remainingAmount": "0",
      "executedAmount": "0.001",
      "avgExecutionPrice": "2800000",
      "status": 2,
      "fee": "0.0000015",
      "feeSymbol": "btc",
      "bitoFee": "0",
      "timeInForce": "GTC",
      "createdTimestamp": 1695900000000,
      "updatedTimestamp": 1695900500000
    }
  ]
}
```

---

## Security

### Never Display Full Secrets

- `BITOPRO_API_KEY`: Show first 5 + last 4 characters only (e.g., `abc12...6789`)
- `BITOPRO_API_SECRET`: Always mask, never display any portion
- `BITOPRO_EMAIL`: Display normally (needed for authentication context)

### Transactions

Before placing or cancelling any order, the agent **must**:

1. Display full order details (pair, side, type, price, amount)
2. Obtain explicit user confirmation before executing

## Agent Behavior

1. **Validate trading pair format** before every request — must be `{base}_{quote}` lowercase with underscore separator.
2. **Handle errors gracefully.** When an API call fails, explain the error to the user and suggest corrective actions.
3. **Respect rate limits.** Public: 600 req/min/IP. Private: 600 req/min/IP + 600 req/min/UID. Create order: 1200 req/min/UID. Cancel order: 900 req/min/UID. Open orders: 5 req/sec/UID.
4. **Market order specifics.** For MARKET BUY orders, the `amount` parameter is in **quote currency** (e.g., TWD), not base currency.
5. **Candlestick timestamps.** Query parameters `from`/`to` are in **seconds**, but response `timestamp` is in **milliseconds**.

## Error Handling

BitoPro error response format:

```json
{
  "error": "error_code",
  "message": "Human-readable error description"
}
```

| HTTP Code | Description |
|-----------|-------------|
| 400 | Bad Request (invalid parameters) |
| 401 | Unauthorized (invalid API key or signature) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found (invalid pair or order ID) |
| 429 | Rate Limit Exceeded |

## User Agent Header

Include in all requests:

```
User-Agent: bitopro-spot/1.0.0 (Skill)
```
