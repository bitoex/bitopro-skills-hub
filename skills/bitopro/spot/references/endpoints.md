# BitoPro API Endpoints Reference

> Base URL: `https://api.bitopro.com/v3`
> Trading pair format: lowercase with underscore, e.g. `btc_twd`, `eth_twd`, `usdt_twd`

---

## Public Endpoints (No Authentication Required)

---

### 1. GET `/tickers/{pair}`

Get real-time ticker data for one or all trading pairs.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | No | Trading pair (e.g. `btc_twd`). Omit to return all pairs. |

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `pair` | string | Trading pair |
| `lastPrice` | string | Latest trade price |
| `high24hr` | string | 24-hour high price |
| `low24hr` | string | 24-hour low price |
| `volume24hr` | string | 24-hour trading volume |
| `priceChange24hr` | string | 24-hour price change (%) |
| `isBuyer` | boolean | Whether the last trade was a buy |

**Example Response:**

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

### 2. GET `/order-book/{pair}`

Get the order book (bid/ask depth) for a trading pair.

| Location | Parameter | Type | Required | Default | Description |
|----------|-----------|------|----------|---------|-------------|
| Path | `pair` | string | Yes | — | Trading pair (e.g. `btc_twd`) |
| Query | `limit` | int | No | 5 | Number of depth levels: `1, 5, 10, 20, 30, 50` |
| Query | `scale` | int | No | 0 | Price aggregation precision (varies by pair) |

**Response Fields (asks / bids arrays):**

| Field | Type | Description |
|-------|------|-------------|
| `price` | string | Price level |
| `amount` | string | Quantity at this level |
| `count` | int | Number of orders at this price level |
| `total` | string | Cumulative quantity |

**Example Response:**

```json
{
  "asks": [
    { "price": "2851000", "amount": "0.12", "count": 3, "total": "0.12" }
  ],
  "bids": [
    { "price": "2849000", "amount": "0.08", "count": 1, "total": "0.08" }
  ]
}
```

---

### 3. GET `/trades/{pair}`

Get recent trade records for a trading pair.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `price` | string | Trade price |
| `amount` | string | Trade quantity |
| `isBuyer` | boolean | Whether the buyer was the maker |
| `timestamp` | integer | Unix timestamp (seconds) |

**Example Response:**

```json
{
  "data": [
    {
      "price": "2850000.00000000",
      "amount": "0.01200000",
      "isBuyer": false,
      "timestamp": 1696000000
    }
  ]
}
```

---

### 4. GET `/trading-history/{pair}`

Get OHLCV candlestick data.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |
| Query | `resolution` | string | Yes | Candlestick interval: `1m, 5m, 15m, 30m, 1h, 3h, 4h, 6h, 12h, 1d, 1w, 1M` |
| Query | `from` | int64 | Yes | Start time (Unix timestamp in **seconds**) |
| Query | `to` | int64 | Yes | End time (Unix timestamp in **seconds**) |

> `1m` and `5m` resolutions only provide data for the last 365 days.

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | number | Unix timestamp (**milliseconds**) |
| `open` | string | Open price |
| `high` | string | High price |
| `low` | string | Low price |
| `close` | string | Close price |
| `volume` | string | Trading volume |

**Example Response:**

```json
{
  "data": [
    {
      "timestamp": 1551052800000,
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

## Private Endpoints (Authentication Required)

All private endpoints require authentication headers. See [auth.md](./auth.md) for details.

**Header rules summary:**
- GET: all three headers included
- POST/PUT: all three headers included
- DELETE: `X-BITOPRO-APIKEY` + `X-BITOPRO-PAYLOAD` + `X-BITOPRO-SIGNATURE`

---

### 5. GET `/accounts/balance`

Get account balances for all currencies.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (none) | — | — | No path or query parameters |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `currency` | string | Currency symbol (e.g. `btc`, `twd`) |
| `amount` | string | Total balance |
| `available` | string | Available balance |
| `stake` | string | Staked amount |
| `tradable` | boolean | Whether the currency is tradable |

**Example Response:**

```json
{
  "data": [
    { "currency": "twd", "amount": "100000", "available": "85000", "stake": "0", "tradable": true },
    { "currency": "btc", "amount": "0.5", "available": "0.3", "stake": "0.2", "tradable": true }
  ]
}
```

---

### 6. POST `/orders/{pair}`

Create a new order (limit / market / stop-limit).

**Rate Limit:** 1200 req / min / UID

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | string | Yes | `BUY` or `SELL` |
| `amount` | string | Yes | Order quantity. For market BUY, this is the quote currency amount (e.g. TWD). |
| `price` | string | Conditional | Required for `LIMIT` and `STOP_LIMIT`. Not required for `MARKET`. |
| `type` | string | Yes | `LIMIT`, `MARKET`, or `STOP_LIMIT` |
| `timestamp` | integer | Yes | Current timestamp in milliseconds |
| `stopPrice` | string | Conditional | Trigger price (only for `STOP_LIMIT`) |
| `condition` | string | Conditional | `>=` or `<=` (only for `STOP_LIMIT`) |
| `timeInForce` | string | No | `GTC` (default) or `POST_ONLY` |
| `clientId` | uint64 | No | Custom order ID (1–2147483647) |
| `percentage` | uint64 | No | Percentage of available balance to sell (1–100) |

**Payload:** `{ action, amount, price, type, timestamp, nonce }` (actual body + nonce, **no `identity`**)

**Example Request Body:**

```json
{
  "action": "BUY",
  "amount": "0.001",
  "price": "2800000",
  "type": "LIMIT",
  "timestamp": 1696000000000
}
```

**Example Response:**

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

---

### 7. DELETE `/orders/{pair}/{orderId}`

Cancel an existing order.

**Rate Limit:** 900 req / min / UID

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |
| Path | `orderId` | string | Yes | Order ID to cancel |

**Payload (used for signature computation, but NOT sent as header):** `{ "identity": email, "nonce": timestamp_ms }`

**Headers:** `X-BITOPRO-APIKEY` + `X-BITOPRO-PAYLOAD` + `X-BITOPRO-SIGNATURE`

**Example Response:**

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

### 8. GET `/orders/open`

Get all open (unfilled or partially filled) orders.

**Rate Limit:** 5 req / sec / UID

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Query | `pair` | string | No | Filter by trading pair. Omit to return all pairs. |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Order ID |
| `pair` | string | Trading pair |
| `action` | string | `BUY` / `SELL` |
| `type` | string | `LIMIT` / `MARKET` / `STOP_LIMIT` |
| `price` | string | Order price |
| `originalAmount` | string | Original order quantity |
| `remainingAmount` | string | Unfilled quantity |
| `executedAmount` | string | Filled quantity |
| `avgExecutionPrice` | string | Average fill price |
| `status` | int | Order status code |
| `fee` | string | Fee amount |
| `feeSymbol` | string | Fee currency |
| `bitoFee` | string | BITO token fee |
| `timeInForce` | string | `GTC` / `POST_ONLY` |
| `createdTimestamp` | int64 | Creation time (ms) |
| `updatedTimestamp` | int64 | Last update time (ms) |

**Example Response:**

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

### 9. GET `/orders/all/{pair}`

Get order history for a trading pair.

| Location | Parameter | Type | Required | Default | Description |
|----------|-----------|------|----------|---------|-------------|
| Path | `pair` | string | Yes | — | Trading pair (e.g. `btc_twd`) |
| Query | `startTimestamp` | int64 | No | 90 days ago | Start time (milliseconds) |
| Query | `endTimestamp` | int64 | No | Now | End time (milliseconds) |
| Query | `statusKind` | string | No | `ALL` | Filter: `OPEN`, `DONE`, `ALL` |
| Query | `status` | int32 | No | — | Specific status code |
| Query | `orderId` | string | No | — | Pagination cursor (returns orders with id <= this value) |
| Query | `limit` | int32 | No | 100 | Results per page (1–1000) |
| Query | `clientId` | int32 | No | — | Filter by custom client ID |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Response:** Same fields as open orders (see above), ordered by creation time descending. Maximum query window is 90 days.

---

## Order Status Codes

| Code | Status |
|------|--------|
| -1 | Not Triggered (stop-limit pending) |
| 0 | In Progress (unfilled) |
| 1 | In Progress (partially filled) |
| 2 | Completed (fully filled) |
| 3 | Completed (partially filled, then cancelled) |
| 4 | Cancelled |
| 6 | Post-Only Cancelled |
