# Fincept Terminal — Release Truth Statement
**Version: 4.0.2**

This document states honestly what is supported, what is partial or experimental,
and what is not yet supported in the current release. It is machine-audited by
`tests/test_capability_matrix.py`.

---

## What the product is

Fincept Terminal is a native Qt/C++ desktop financial terminal with a Python sidecar.
It provides market data, portfolio management, paper trading, AI-assisted analysis,
and connections to live brokers. A Python subprocess handles data fetching, LLM
orchestration, and advanced quant computation.

---

## Fully Supported (production-quality behavior)

| Feature | Notes |
|---------|-------|
| Market Data — yfinance / ccxt / AKShare | REST polling; live-streaming via broker websockets |
| Portfolio tracking | Positions, P&L, allocations |
| Paper Trading (limit/stop orders) | Requires caller-supplied `market_price` for market orders |
| Broker connectivity — Fyers, Motilal, AngelOne | OAuth/API-key flow implemented |
| AI chat (OpenAI / Anthropic) | Requires user-supplied API key |
| News feed | Multiple sources via feedparser + gnews |
| Economics data | Central bank REST adapters (BNM, TCM, BOC, etc.) |
| Theme / UI | Dark terminal theme, responsive layout |
| MCP tool server | Tool registration and dispatch working |

---

## Partial / Experimental (use with caution)

| Feature | Status | Limitation |
|---------|--------|------------|
| Kalshi prediction market | Experimental | WebSocket live feed is a stub (future phase); REST polling works |
| Polymarket | Partial | Order placement and some read paths not implemented; stub_unsupported() is called |
| Surface Analytics | Demo | Volatility surface is populated with synthetic demo data when no live source is connected |
| VisionQuant pattern engine | Experimental | Requires optional quant pack; behavior not fully validated |
| GluonTS / functime forecasting | Experimental | Requires NumPy 1.x env; not tested in CI |
| RL trading agents (SB3) | Experimental | Scaffolding present; no trained models shipped |

---

## Not Supported / Planned

| Feature | Notes |
|---------|-------|
| Kalshi WebSocket live streaming | Planned (Phase 7) |
| Polymarket full order lifecycle | Planned |
| Live speech-to-text trading | Planned; PyAudio dependency not in core env |
| Multi-account broadcast (live) | Paper only tested |

---

## Paper Trading Guarantee

No paper order will ever fabricate a fill price. Market orders **must** supply a
`market_price` field > 0. If the field is absent or zero, the order is rejected
with a descriptive error. This is enforced in `UnifiedTrading.cpp` and tested
by `tests/test_no_fabricated_price.py`.
