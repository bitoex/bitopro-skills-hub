# BitoPro Coin Mapping

Complete mapping between BitoPro symbols, CoinGecko IDs, and CoinPaprika IDs.

> Last verified: 2026-04-14 (MV removed — delisting decided)

## Full Mapping Table

| BitoPro Symbol | Name | CoinGecko ID | CoinPaprika ID | Notes |
|----------------|------|-------------|----------------|-------|
| BTC | Bitcoin | `bitcoin` | `btc-bitcoin` | |
| ETH | Ethereum | `ethereum` | `eth-ethereum` | |
| USDT | Tether | `tether` | `usdt-tether` | Stablecoin |
| USDC | USD Coin | `usd-coin` | `usdc-usd-coin` | Stablecoin |
| XRP | XRP | `ripple` | `xrp-xrp` | |
| SOL | Solana | `solana` | `sol-solana` | |
| BNB | BNB | `binancecoin` | `bnb-binance-coin` | |
| DOGE | Dogecoin | `dogecoin` | `doge-dogecoin` | |
| ADA | Cardano | `cardano` | `ada-cardano` | |
| TRX | TRON | `tron` | `trx-tron` | |
| TON | Toncoin | `the-open-network` | `ton-toncoin` | |
| LTC | Litecoin | `litecoin` | `ltc-litecoin` | |
| BCH | Bitcoin Cash | `bitcoin-cash` | `bch-bitcoin-cash` | |
| SHIB | Shiba Inu | `shiba-inu` | `shib-shiba-inu` | |
| POL | POL (ex-MATIC) | `polygon-ecosystem-token` | `matic-polygon` | CoinPaprika still uses old MATIC ID |
| APE | ApeCoin | `apecoin` | `ape-apecoin` | |
| KAIA | Kaia | `kaia` | `kaia-kaia` | Formerly Klaytn (KLAY) |
| BITO | BITO Coin | `bito-coin` | `bito-bito-coin` | BitoPro exchange token — low liquidity, CoinGecko may return `market_cap_rank: null` |

## CoinGecko IDs (comma-separated, for API calls)

```
bitcoin,ethereum,tether,ripple,binancecoin,usd-coin,solana,dogecoin,cardano,tron,the-open-network,litecoin,bitcoin-cash,shiba-inu,polygon-ecosystem-token,apecoin,kaia,bito-coin
```

## BitoPro Symbol Set (for filtering)

```
BTC,ETH,USDT,USDC,XRP,SOL,BNB,DOGE,ADA,TRX,TON,LTC,BCH,SHIB,POL,APE,KAIA,BITO
```

## BitoPro Trading Pairs

As of 2026-04-14, BitoPro has active trading pairs across TWD and USDT quote currencies for the 18 base coins above.

### TWD Pairs
BTC_TWD, ETH_TWD, USDT_TWD, USDC_TWD, XRP_TWD, SOL_TWD, BNB_TWD, DOGE_TWD, ADA_TWD, TRX_TWD, TON_TWD, LTC_TWD, BCH_TWD, SHIB_TWD, POL_TWD, APE_TWD, KAIA_TWD, BITO_TWD

### USDT Pairs
BTC_USDT, ETH_USDT, XRP_USDT, SOL_USDT, BNB_USDT, DOGE_USDT, ADA_USDT, TRX_USDT, TON_USDT, LTC_USDT, BCH_USDT, SHIB_USDT, POL_USDT, APE_USDT, KAIA_USDT

> Always call Tool 7 (`get_bitopro_pairs`) with `Accept: application/json` header to verify live pair availability — the hard-coded list above is for reference only.

## Updating This Mapping

When BitoPro adds new coins:

1. Call `GET https://api.bitopro.com/v3/provisioning/trading-pairs` to get updated list
2. For new coins, find CoinGecko ID via `GET https://api.coingecko.com/api/v3/search?query={coin_name}`
3. For CoinPaprika, search via `GET https://api.coinpaprika.com/v1/search?q={coin_name}`
4. Update this mapping file

## Known Discrepancies

- **POL/MATIC**: CoinGecko uses `polygon-ecosystem-token` (new name), CoinPaprika still uses `matic-polygon` (old name). Both resolve to the same asset.
- **KAIA/KLAY**: Formerly Klaytn, rebranded to Kaia. Both CoinGecko and CoinPaprika now use Kaia IDs.
- **BITO**: BitoPro's exchange token. CoinGecko often returns `market_cap_rank: null` and `market_cap: 0`. Display rank as `—` and still show price + 24h change.

## Removed / Delisted

- **MV (GensoKishi Metaverse)**: Removed from this mapping on 2026-04-14 following BitoPro's delisting decision. If the BitoPro `/v3/provisioning/trading-pairs` endpoint still temporarily lists MV pairs during the wind-down window, ignore them.
