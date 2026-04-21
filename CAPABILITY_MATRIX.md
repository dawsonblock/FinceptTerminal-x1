# Fincept Terminal — Capability Matrix
**Version: 4.0.2**

Status definitions:
- **supported** — fully implemented, tested, production-safe
- **partial** — some paths implemented; known gaps exist
- **experimental** — works in dev but not hardened; may change
- **demo** — uses synthetic/generated data; not live
- **planned** — scaffolding or stub; not yet functional

---

## UI Screens

| Screen | Status | Notes |
|--------|--------|-------|
| Dashboard | supported | |
| Market Data | supported | |
| Portfolio | supported | |
| Trading (Paper) | supported | Requires market_price for market orders |
| Paper Trading (Market Orders) | supported | Caller must supply market_price > 0; rejected otherwise |
| Trading (Live) | partial | Fyers/Motilal/AngelOne only; other brokers partial |
| AI Quant Lab | experimental | Requires optional-ai pack |
| Surface Analytics | demo | Volatility surface uses synthetic demo data |
| Economics | supported | Multiple central bank REST sources |
| News | supported | |
| Docs | supported | |
| Workspace | supported | |
| Chat Mode | experimental | LLM routing works; some tool paths partial |

---

## Broker Adapters

| Broker | Status | Notes |
|--------|--------|-------|
| Fyers | supported | Auth + order placement tested |
| Motilal Oswal | supported | Auth + order placement tested |
| AngelOne | partial | Order placement present; cancel/modify partial |
| Upstox | partial | REST implemented; websocket partial |
| Zerodha | planned | Scaffold present |
| Interactive Brokers | planned | Not implemented |
| Alpaca | planned | Not implemented |

---

## Market Data Sources

| Source | Status | Notes |
|--------|--------|-------|
| yfinance | supported | |
| ccxt (crypto) | supported | |
| AKShare | supported | |
| Databento | partial | Requires optional pack + API key |
| EDGAR (SEC) | partial | Requires optional pack |
| Central bank adapters | supported | BNM, TCM, BOC, Norges, Riksbank, etc. |

---

## Prediction Markets

| Adapter | Status | Notes |
|---------|--------|-------|
| Kalshi (REST) | experimental | Auth + market fetch work; order paths partial |
| Kalshi (WebSocket) | planned | Stub only; Phase 7 |
| Polymarket | partial | Read paths partial; order placement stubbed |

---

## Python Quant / AI Features

| Feature | Status | Notes |
|---------|--------|-------|
| OpenAI / Anthropic chat | supported | Requires core pack + user API key |
| Google Gemini | experimental | Requires optional-ai pack |
| LangChain | experimental | Requires optional-ai pack |
| Backtesting (vectorbt/zipline) | experimental | Requires optional-quant NumPy 1.x env |
| Portfolio optimization (PyPortfolioOpt) | experimental | Requires optional-quant |
| GluonTS forecasting | experimental | Requires optional-quant |
| RL agents (SB3) | experimental | No trained models shipped |
| VisionQuant | experimental | Requires optional-quant |
| Speech-to-text | planned | PyAudio not in core env |

---

## Infrastructure

| Component | Status | Notes |
|-----------|--------|-------|
| PythonRunner (C++ sidecar) | supported | |
| MCP tool server | supported | |
| Secure credential store | supported | |
| Auto-updater | supported | updates.json schema v2 |
| QuantLib integration | partial | User-agent and REST calls; full SDK not in core |
| Workflow engine | experimental | Node graph present; not all nodes hardened |
