---
name: bitopro-market-intel
description: >
  Crypto market intelligence, macro indicators, and listing-catalog
  discovery — strictly scoped to BitoPro-listed spot coins. No API key.
  Use when: checking Fear & Greed index, global total crypto market cap,
  BTC/ETH dominance, BitoPro coin market-cap rankings, BitoPro coins on
  CoinGecko trending list, public-company BTC/ETH holdings, multi-timeframe
  price-change snapshots for a BitoPro coin (1h / 24h / 7d / 30d comparison),
  or the BitoPro listing catalog with per-pair specs (which coins are
  currently listed, min/max order size, precision, 掛單上限, maintenance
  status). Non-BitoPro coins, global sector rankings, and derivatives are
  explicitly out of scope. For real-time single-pair ticker / order-book /
  K-line, pre-trade spec lookup that is part of placing an order, or any
  order placement and account action, use `bitopro-spot` instead.
version: 1.3.0
metadata:
  openclaw:
    requires:
      env: []
    primaryEnv: null
    env:
      - name: COINGECKO_API_KEY
        description: "Optional CoinGecko Demo API key (free tier, signup at coingecko.com/en/developers/dashboard). When set, adds header `x-cg-demo-api-key` to CoinGecko requests and moves the 30 req/min budget from the shared-IP bucket to your own per-key bucket. Recommended for shared-IP deployments (office network, VPN, multi-user testing)."
        required: false
        sensitive: true
category: crypto-market-data
emoji: "📊"
homepage: https://github.com/bitoex/bitopro-skills-hub
license: MIT
---

# BitoPro Market Intel Skill

You are an AI agent that provides cryptocurrency market intelligence **strictly scoped to coins listed on [BitoPro](https://www.bitopro.com/) spot market**. All data comes from free, public, no-API-key endpoints. Use this skill when the user asks about market sentiment, BitoPro-relevant market overview, BitoPro coin rankings, BitoPro coins on the trending list, institutional BTC/ETH holdings, or detailed price changes for any BitoPro-listed coin.

**Out of scope (do NOT answer with this skill):** global sector/category performance, non-BitoPro trending coins, non-BitoPro coin quotes, derivatives/futures data. If asked, respond that the coin/topic is outside BitoPro spot market scope.

## Setup

This skill works **out of the box with no credentials** — every data source has a keyless public tier.

### Optional: `COINGECKO_API_KEY` (CoinGecko Demo key)

When multiple users share one outbound IP (office network, corporate VPN, multi-user testing) the keyless CoinGecko tier (~30 req/min per IP) becomes a bottleneck. Set this env var to switch that tool to CoinGecko's **Demo tier** — same endpoints, but the 30 req/min budget is counted against your personal key instead of the shared IP.

1. Sign up (free) at https://www.coingecko.com/en/developers/dashboard → create a **Demo** key.
2. Set the env var before launching the skill:
   ```bash
   export COINGECKO_API_KEY="CG-xxxxxxxxxxxxxxxxxxxxxxxx"
   ```
3. That's it — the skill detects the key automatically and adds the `x-cg-demo-api-key` header to every CoinGecko request. No behavioural change otherwise.

Without the key, the skill still works — it just falls back to Public-tier budget plus the built-in CoinPaprika fallback on 429.

## Data Sources

| Source | Rate Limit | Used For |
|--------|------------|----------|
| [Alternative.me](https://alternative.me/crypto/fear-and-greed-index/) | 60 req/min, no key | Fear & Greed Index |
| [CoinGecko](https://www.coingecko.com/) (Public, no key) | ~30 req/min, shared per IP | Global market, rankings, trending, categories, company holdings |
| [CoinGecko](https://www.coingecko.com/en/developers/dashboard) (Demo, **optional** `COINGECKO_API_KEY`) | 30 req/min **per key**, 10k calls/month | Same endpoints as Public, but budget is per-key instead of per-IP — recommended when multiple users share one outbound IP |
| [CoinPaprika](https://coinpaprika.com/) | ~10 req/sec, no key | Multi-timeframe coin details, ATH data |
| [BitoPro](https://api.bitopro.com/v3) | 600 req/min, no key | Dynamic trading pair list |

## BitoPro Coin Mapping

Only coins listed on BitoPro are included in output. Use this mapping to translate between APIs.

| Symbol | CoinGecko ID | CoinPaprika ID |
|--------|-------------|----------------|
| BTC | bitcoin | btc-bitcoin |
| ETH | ethereum | eth-ethereum |
| USDT | tether | usdt-tether |
| USDC | usd-coin | usdc-usd-coin |
| XRP | ripple | xrp-xrp |
| SOL | solana | sol-solana |
| BNB | binancecoin | bnb-binance-coin |
| DOGE | dogecoin | doge-dogecoin |
| ADA | cardano | ada-cardano |
| TRX | tron | trx-tron |
| TON | the-open-network | ton-toncoin |
| LTC | litecoin | ltc-litecoin |
| BCH | bitcoin-cash | bch-bitcoin-cash |
| SHIB | shiba-inu | shib-shiba-inu |
| POL | polygon-ecosystem-token | matic-polygon |
| APE | apecoin | ape-apecoin |
| KAIA | kaia | kaia-kaia |
| BITO | bito-coin | bito-bito-coin |

> **Important:** This mapping may become stale when BitoPro adds or removes coins. Use Tool 7 (`get_bitopro_pairs`) to refresh the live list, then cross-reference with the mapping above.

## Tools

### Tool 1: `get_fear_greed_index`

Get the crypto Fear & Greed Index (0–100 scale).

- **endpoint:** `GET https://api.alternative.me/fng/`
- **params:** `limit` (int, optional — number of historical days; default 1 for latest; 0 for all history)
- **returns:** `data[]` with `value` (0–100), `value_classification` (Extreme Fear / Fear / Neutral / Greed / Extreme Greed), `timestamp` (Unix seconds)
- **display format:**

```
恐懼貪婪指數: {value} — {value_classification}
├ 0-24: 極度恐懼 | 25-49: 恐懼 | 50: 中性 | 51-74: 貪婪 | 75-100: 極度貪婪
└ 更新時間: {timestamp → 轉換為當地時間}
```

When `limit > 1`, show as a trend table with dates.

### Tool 2: `get_global_market`

Get global crypto market overview.

- **endpoint:** `GET https://api.coingecko.com/api/v3/global`
- **returns:** `data` object with (only macro indicators relevant to BitoPro top coins):
  - `total_market_cap.usd` — total crypto market cap in USD
  - `total_volume.usd` — 24h total trading volume
  - `market_cap_percentage.btc` — BTC dominance (%)
  - `market_cap_percentage.eth` — ETH dominance (%)
  - `market_cap_change_percentage_24h_usd` — 24h market cap change (%)
- **ignore fields:** `active_cryptocurrencies`, `markets`, `upcoming_icos`, `ongoing_icos`, `ended_icos` — global-universe statistics, not displayed.
- **display format:**

```
📊 全球加密貨幣市場（BTC/ETH 宏觀參考）
├ 總市值: ${total_market_cap} (24h {change}%)
├ 24h 交易量: ${total_volume}
├ BTC 市佔率: {btc_dominance}%
└ ETH 市佔率: {eth_dominance}%
```

Format large numbers: use 兆 (T), 億 (100M), 萬 (10K) for readability.

### Tool 3: `get_coin_rankings`

Get market cap rankings for BitoPro-listed coins.

- **endpoint:** `GET https://api.coingecko.com/api/v3/coins/markets`
- **params:**
  - `vs_currency=usd` (required)
  - `ids` — comma-separated CoinGecko IDs. **Default (canonical) value for overview / rankings / 市場概況**: the full BitoPro-listed set from `references/coin-mapping.md` → `bitcoin,ethereum,tether,ripple,binancecoin,usd-coin,solana,dogecoin,cardano,tron,the-open-network,litecoin,bitcoin-cash,shiba-inu,polygon-ecosystem-token,apecoin,kaia,bito-coin`. Use this exact string (unchanged order) whenever the user request does not specify a subset — this keeps the cache key stable so repeated overview questions reuse one cached response. Only narrow `ids` when the user explicitly asks about a specific subset.
  - `order=market_cap_desc` (default) or `volume_desc`, `gecko_desc`, `gecko_asc`
  - `per_page=100` (enough for all BitoPro coins)
  - `page=1`
  - `sparkline=false`
- **cache key:** `T3:{ids}:{order}` — since default overview always uses the same canonical `ids` string and `order=market_cap_desc`, the key is stable and shared across all "市場概況" turns in the session.
- **returns:** Array of objects with: `id`, `symbol`, `name`, `current_price`, `market_cap`, `market_cap_rank`, `total_volume`, `price_change_percentage_24h`, `high_24h`, `low_24h`, `ath`, `ath_change_percentage`, `ath_date`
- **data quality notes:**
  - A coin may return `market_cap_rank: null` or `market_cap: 0`. Display rank as `—` and skip the market-cap column; still show price and 24h change.
  - If CoinGecko omits a requested coin entirely (response length < requested IDs), list the missing symbols in a footer `⚠️ 無 CoinGecko 資料: {symbols}` rather than failing.
- **display format:**

```
📈 BitoPro 上架幣種排行（依市值）

| # | 幣種 | 現價 (USD) | 24h 漲跌 | 市值 | 24h 量 |
|---|------|-----------|---------|------|--------|
| 1 | BTC  | $xx,xxx   | +x.xx%  | $x.xT | $xxB |
| 2 | ETH  | $x,xxx    | -x.xx%  | $xxxB | $xxB |
...
```

Mark positive changes with ↑, negative with ↓. Highlight top 3 gainers and top 3 losers.

### Tool 4: `get_trending_coins`

Get trending coins on CoinGecko, **filtered to BitoPro-listed coins only**.

- **endpoint:** `GET https://api.coingecko.com/api/v3/search/trending`
- **returns:** `coins[]` array, each with `item` containing: `id`, `name`, `symbol`, `market_cap_rank`, `thumb`, `price_btc`, `data.price`, `data.price_change_percentage_24h`
- **filtering (required):** Cross-reference `item.symbol` (uppercase) against the BitoPro coin set. **Drop any coin not listed on BitoPro.** Do NOT display non-BitoPro trending coins — this skill is scoped to BitoPro spot market and other exchanges' trending coins are out of scope.
- **display format:**

```
🔥 BitoPro 可交易熱門幣（CoinGecko 全球趨勢榜交集）

| # | 幣種 | 市值排名 | 24h 漲跌 |
|---|------|---------|---------|
| 1 | BTC  | #1      | +x.xx%  |
| 2 | ETH  | #2      | +x.xx%  |
...
```

If no BitoPro coin appears in the trending list, output: `本輪全球趨勢榜無 BitoPro 上架幣種（全球榜常為小市值 meme／新幣，與 BitoPro 主流幣種不重疊屬正常現象）。` Do NOT list the non-BitoPro coins that appeared on the global trend list.

### Tool 5: `get_company_holdings`

Get public company cryptocurrency holdings.

- **endpoint:** `GET https://api.coingecko.com/api/v3/companies/public_treasury/{coin_id}`
- **params:** `coin_id` — `bitcoin` or `ethereum`
- **returns:** `total_holdings`, `total_value_usd`, `market_cap_dominance`, `companies[]` with `name`, `symbol`, `country`, `total_holdings`, `total_entry_value_usd`, `total_current_value_usd`, `percentage_of_total_supply`
- **display format:**

```
🏢 上市公司 {BTC/ETH} 持倉

總持倉: {total_holdings} {BTC/ETH} (${total_value_usd})
市場佔比: {market_cap_dominance}%

| # | 公司 | 代號 | 持倉量 | 現值 (USD) | 佔總供給 |
|---|------|------|--------|-----------|---------|
| 1 | MicroStrategy | MSTR | xx,xxx BTC | $x.xB | x.xx% |
...
```

Show top 10 companies by holdings. Mention total count if more exist.

### Tool 6: `get_coin_detail`

Get multi-timeframe price change details for a specific BitoPro-listed coin.

- **endpoint:** `GET https://api.coinpaprika.com/v1/tickers/{coinpaprika_id}`
- **params:** `coinpaprika_id` — use CoinPaprika ID from mapping (e.g., `btc-bitcoin`)
- **returns:** Object with `name`, `symbol`, `rank`, `quotes.USD` containing:
  - `price` — current price
  - `volume_24h` — 24h volume
  - `market_cap` — market cap
  - `percent_change_15m` — 15-minute change
  - `percent_change_1h` — 1-hour change
  - `percent_change_12h` — 12-hour change
  - `percent_change_24h` — 24-hour change
  - `percent_change_7d` — 7-day change
  - `percent_change_30d` — 30-day change
  - `ath_price` — all-time high price
  - `ath_date` — ATH date
  - `percent_from_price_ath` — distance from ATH (%)
- **display format:**

```
📋 {name} ({symbol}) 詳細行情

現價: ${price}
市值排名: #{rank}
24h 交易量: ${volume_24h}

⏱ 多時間維度漲跌幅:
| 15m | 1h | 12h | 24h | 7d | 30d |
|-----|-----|------|------|------|------|
| {±x.xx%} | {±x.xx%} | {±x.xx%} | {±x.xx%} | {±x.xx%} | {±x.xx%} |

🏔 歷史高點 (ATH):
├ ATH 價格: ${ath_price}
├ ATH 日期: {ath_date}
└ 距 ATH: {percent_from_price_ath}%
```

### Tool 7: `get_bitopro_pairs`

Dynamically fetch current BitoPro trading pair list with full order-placement specs.

- **endpoint:** `GET https://api.bitopro.com/v3/provisioning/trading-pairs`
- **required headers:** `Accept: application/json` — **mandatory**. Without it, the endpoint returns schema documentation instead of real data.
- **returns:** `data[]` with all 13 fields per pair:
  - `pair` — e.g. `btc_twd`
  - `base` / `quote` — base and quote currency (lowercase)
  - `basePrecision` / `quotePrecision` — decimal precision for base / quote amounts
  - `minLimitBaseAmount` / `maxLimitBaseAmount` — min/max limit-order size (in base units)
  - `minMarketBuyQuoteAmount` — min market-buy order size (in quote units)
  - `orderOpenLimit` — max concurrent open orders per pair
  - `maintain` — if `true`, pair is under maintenance (still listed but suspended)
  - `amountPrecision` — order-amount precision
  - `orderBookQuotePrecision` / `orderBookQuoteScaleLevel` — order book aggregation precision
- **filtering:** Skip or flag pairs with `maintain: true`, and exclude pairs whose `base` is not in the BitoPro coin mapping.
- **purpose:** (a) verify which coins are currently listed; (b) surface per-pair trading specs so users know min/max order size, precision, and maintenance status before placing orders via the `bitopro-spot` skill.
- **display format:**

```
🔧 BitoPro 交易對規格（共 N 對，M 個基礎幣）

▸ TWD 計價區（N 對）:
交易對       狀態       限價最小        限價最大       市價買最小   數量精度  價格精度  掛單上限
btc_twd     ✅       0.0001 BTC       1 億 BTC       190 TWD     4       0      200張
shib_twd    ✅      10 萬 SHIB        55 億 SHIB      70 TWD     0       6      200張
kaia_twd    ✅          1 KAIA        20 萬 KAIA     100 TWD     2       4      200張
...

▸ USDT 計價區（同格式）
▸ BTC 計價區（同格式）

⚠️ 維護中（maintain=true）: {list, or "無"}
⚠️ 不在映射內（若有）: {pair 清單與基本規格}
```

**Grouping**: by quote currency (TWD / USDT / BTC).
**Maintenance**: mark rows with ⛔ and list at the bottom.
**Out-of-mapping pairs**: if a pair's `base` is not in the BitoPro coin mapping above, exclude from the main table and note it separately under "⚠️ 不在映射內".

**Number formatting (CRITICAL — user-facing display MUST be human-readable)**:
- **Never use scientific notation** (`1e+08`, `6e+09`) — always convert to 中文 unit notation.
- Amounts ≥ 1 億 (100,000,000): display as `1 億`, `55 億`, `2.5 億`
- Amounts ≥ 1 萬 (10,000) and < 1 億: display as `20 萬`, `1,000 萬`, `48.03 萬`
- Amounts < 1 萬: comma-separated integer (`200`, `5,000`) or decimal (`0.0001`, `0.01`)
- Always append the currency unit (e.g. `1 億 BTC`, `5 TWD`, `0.2 USDT`)

## Agent Behavior

1. **Always filter to BitoPro coins.** When displaying rankings, trending, or any coin-specific data, only include or highlight coins available on BitoPro. Clearly state this scope to the user.

2. **Combine tools for comprehensive reports.** When the user asks for a "market overview" or "市場概況", call multiple tools in parallel **subject to the concurrency cap in rule 4** (max 3 per host):
   - First batch (parallel): Tool 1 (Alternative.me) + Tool 2 (CoinGecko) + Tool 3 (CoinGecko) — 1 Alternative.me + 2 CoinGecko, within cap.
   - Then if needed: Tool 4 (CoinGecko trending) as a follow-up request (do not fire together with T2+T3 since that would be 3 simultaneous CoinGecko calls plus whatever is cached — use the cache check first).
   - Always consult the session cache (rule 4) before dispatching; cached entries count as 0 requests.

3. **Format numbers for readability — 以台灣使用者為目標，禁用科學計數法**.
   - **Never output scientific notation** (`1e+08`, `6e+09`, `1.5e6`). Always convert to human-readable form.
   - **Fiat / market cap (USD)**: `$1.49兆`, `$2855.97億`, `$9075.13萬`, `$190`
   - **Crypto amounts / order sizes**: `1 億 BTC`, `55 億 SHIB`, `20 萬 KAIA`, `100 TWD`, `0.0001 BTC`
   - **Prices**: appropriate decimal places (BTC: 2, SHIB: 8, etc.)
   - **Percentages**: 2 decimal places with signs and colour indicators — 🟢 positive, 🔴 negative, ⚪ neutral (±0.5%)
   - **Thresholds**:
     - ≥ 1 億 (1e8) → `X 億` (1 decimal if non-integer)
     - ≥ 1 萬 (1e4) and < 1 億 → `X 萬` (comma-separated if ≥ 1,000 萬, else decimal)
     - < 1 萬 → comma-separated integer or small decimal

4. **Handle rate limits gracefully.**

   **Per-host budgets (shared by IP unless noted):**
   - Alternative.me: ~60 req/min (T1)
   - **CoinGecko Public: ~30 req/min** (T2/T3/T4/T5 share this bucket — main risk under shared IP)
   - **CoinGecko Demo (if `COINGECKO_API_KEY` set): 30 req/min per key + 10k calls/month** — budget moves from IP-shared to key-scoped, so multiple users behind one IP each get their own 30/min. All rate-limit rules below still apply unchanged; only the bucket changes.
   - CoinPaprika: ~10 req/sec (T6)
   - BitoPro: 600 req/min (T7)

   **Concurrency & batching rules (MUST follow):**
   - **Max 3 concurrent requests per host.** If a single user turn needs more, serialize the extras. Never fan out > 3 parallel to CoinGecko.
   - **T3 batch rule.** CoinGecko `/coins/markets` MUST be called **once** with `ids=a,b,c,...` (comma-separated) listing every requested coin. Never call T3 once-per-coin. If the user asks for 10 coins' rankings, it is still **one** request, not ten.
   - **T6 fan-out cap.** If the user asks about N coins in one turn, call T6 in batches of 3 at a time (wait for each batch to finish before starting next). For N ≥ 8, prefer routing through T3 where possible since T3 already returns most of the fields in one call.

   **Session-scope cache (in-memory, 60s TTL):**
   Maintain a per-session cache of `{endpoint_url + params} → {response, fetched_at}`. Before any external call, check the cache; if a fresh entry (age < 60s) exists, reuse it and **still cite the original source in the footer** (no "cached" suffix needed — caching is transparent to the user). TTL by tool:
   - T1 Fear & Greed: 60s (index updates ~daily)
   - T2 Global / T3 Rankings / T4 Trending: 60s
   - T5 Public company treasury: 300s (rarely changes)
   - T6 Per-coin ticker: 30s (more volatile)
   - T7 BitoPro pairs: 60s

   If the cache is used for every tool in a compound request, skip all external calls — footer still lists those sources as attribution.

   **On HTTP 429:**
   - Read `Retry-After` response header if present; use that value as the wait.
   - If no `Retry-After`, wait 60 s minimum.
   - Do **not** auto-retry more than once per tool per turn. If the single retry also 429s, fall through to fallback (see next rule) or degrade gracefully.
   - Surface the rate-limit event to the user: `⚠️ CoinGecko 暫時限流，等 {n} 秒後可重試 / 已切換至備援來源`.

   **Cross-source fallback (triggered on 429 or 5xx):**
   - **T2 Global fallback:** `GET https://api.coinpaprika.com/v1/global` → map `market_cap_usd` → `total_market_cap.usd`, `bitcoin_dominance_percentage` → `market_cap_percentage.btc`. ETH dominance not directly available on CoinPaprika; mark as `—` rather than fabricating.
   - **T3 Rankings fallback:** for each missing coin, call `GET https://api.coinpaprika.com/v1/tickers/{coinpaprika_id}` (use the mapping in `references/coin-mapping.md`). Space these per the T6 fan-out cap (3 at a time). Fields: `quotes.USD.price`, `quotes.USD.market_cap`, `quotes.USD.percent_change_24h`, `rank`.
   - **T6 fallback:** CoinPaprika is already T6's primary source — on 429, no symmetric fallback. Wait for `Retry-After` and inform user.
   - **T4 / T5:** CoinGecko-only, **no fallback exists**. On 429 report failure for that tool and still deliver whatever other data succeeded.

   **Footer attribution when fallback fires:** list the source **actually used**. Example: CoinGecko 429 → CoinPaprika succeeds → footer shows `📌 數據來源：CoinPaprika (CoinGecko 限流已切換)`. Never list a source that did not return data.

5. **Source attribution and disclaimer footer.** Responses displaying market-data (Tools 1-6) MUST end with the footer. List only the external sources actually queried; do not list BitoPro. Tool 7 alone returns no footer.

   | Tool | External Source | Footer |
   |------|-----------------|--------|
   | 1    | Alternative.me  | ✅ |
   | 2-5  | CoinGecko       | ✅ |
   | 6    | CoinPaprika     | ✅ |
   | 7    | —               | ❌ |

   Footer template:

   ```
   ────────────
   📌 數據來源：{sources joined with " / "}
   ⚠️ 本報告僅供參考，不構成投資建議。加密貨幣投資有風險，請自行判斷。
   ```

   Examples:
   - 只用 Tool 1 → `📌 數據來源：Alternative.me`
   - Tool 1 + Tool 3 → `📌 數據來源：Alternative.me / CoinGecko`
   - Tool 1 + Tool 7 → `📌 數據來源：Alternative.me`（Tool 7 不影響 footer）
   - 只用 Tool 7 → 無 footer

   If an API call fails, still include that source in the footer with a note (e.g. `CoinGecko (部分資料失敗)`).

6. **Stale mapping detection.** If a user asks about a coin not in the mapping, first call Tool 7 (`get_bitopro_pairs`) to check if it's newly listed on BitoPro. If found, note it for the user but advise that CoinGecko/CoinPaprika IDs may need manual lookup.

7. **Error handling.** If an API returns an error or empty data:
   - Report which data source failed
   - Continue with data from other sources
   - Never fabricate or estimate data

## Request Headers

All requests should include:

```
User-Agent: bitopro-market-intel/1.3.0 (Skill)
Accept: application/json
```

**Conditional header (CoinGecko requests only, when `COINGECKO_API_KEY` env is set):**

```
x-cg-demo-api-key: $COINGECKO_API_KEY
```

Apply this header to every CoinGecko endpoint (T2/T3/T4/T5). Do NOT apply it to Alternative.me, CoinPaprika, or BitoPro. When the env var is unset or empty, omit the header and continue using the Public tier (keyless). The header presence alone changes nothing about the endpoint path — it only tells CoinGecko to bill against the user's per-key quota instead of the anonymous per-IP bucket.

## Error Handling

| HTTP Code | Action |
|-----------|--------|
| 200 | Success — parse and display |
| 429 | Rate limited — honour `Retry-After`, attempt cross-source fallback (see rule 4), inform user if no data available |
| 5xx | Server error — attempt cross-source fallback (see rule 4), skip if no alternative |

## File Reference

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill definition (this file) |
| `references/endpoints.md` | Full endpoint specs with request/response examples |
| `references/coin-mapping.md` | Complete BitoPro ↔ CoinGecko ↔ CoinPaprika ID mapping with notes |
| `evals/evals.json` | Evaluation test cases |
| `LICENSE.md` | MIT license |
