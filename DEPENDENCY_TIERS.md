# Fincept Terminal — Dependency Tiers
**Version: 4.0.2**

## Overview

The Python sidecar is split into three dependency tiers to reduce
installation surface, improve reproducibility, and allow optional
features to degrade gracefully instead of crashing the whole app.

---

## Tier 1 — Core Runtime (`requirements-core.txt`)

**Required for the app to launch and run its main workflows.**

Install with:
```bash
pip install -r fincept-qt/resources/requirements-core.txt
```

Includes:
- `numpy`, `pandas` — data foundations
- `requests`, `aiohttp`, `websockets` — networking
- `yfinance`, `ccxt`, `akshare` — essential market data
- `feedparser` — news feeds
- `openai`, `anthropic` — AI chat gateway
- `agno` — AI orchestration framework
- `loguru`, `pydantic-settings` — utilities

**What works with only Tier 1:** market data, portfolio, paper trading,
live broker connectivity (Fyers/Motilal), AI chat, news, economics screens.

---

## Tier 2 — Optional AI / LLM Pack (`requirements-optional-ai.txt`)

**Install to unlock advanced AI and ML research features.**

Install with:
```bash
pip install -r fincept-qt/resources/requirements-optional-ai.txt
```

Adds:
- Google Gemini, LangChain, tiktoken
- PyTorch, scikit-learn, scipy, lightgbm, xgboost, catboost
- Deep research agents (rdagent, deepagents, gs-quant)
- Speech recognition (SpeechRecognition, PyAudio)
- MLflow experiment tracking
- Streamlit, weasyprint (report generation)

**What degrades if absent:** Gemini/LangChain AI features show
"AI pack not installed" in the UI. ML model features unavailable.
Core market data and trading continue to work.

---

## Tier 3 — Optional Quant Pack (`requirements-optional-quant.txt`)

**Install in a NumPy 1.x virtual environment for backtesting and
advanced quantitative analysis.**

> ⚠️ These packages require `numpy < 2.0`. Use a separate virtual
> environment from Tier 1 / Tier 2.

Install with:
```bash
pip install -r fincept-qt/resources/requirements-optional-quant.txt
```

Adds:
- `vectorbt`, `zipline-reloaded`, `backtesting` — backtesting engines
- `numba`, `financepy` — financial modeling
- `PyPortfolioOpt`, `cvxpy` — portfolio optimization
- `stable-baselines3`, `gymnasium` — RL agents
- `faiss-cpu`, `mplfinance` — VisionQuant
- `py-clob-client`, `eth-account` — Polymarket/Kalshi (EXPERIMENTAL)
- `databento`, `vnpy`, `edgartools` — advanced data sources

**What degrades if absent:** Quant Lab, VisionQuant, backtesting,
and prediction market trading show "Quant pack not installed" in UI.
All Tier 1 features continue to work.

---

## Graceful Degradation Contract

Python-heavy features must catch `ImportError` and surface a clear UI
message rather than crashing the sidecar process. Example pattern:

```python
try:
    import vectorbt as vbt
except ImportError:
    raise RuntimeError(
        "Backtesting features require the optional quant pack. "
        "Install: pip install -r requirements-optional-quant.txt"
    )
```

C++ callers receive the error string via `PythonRunner` and display it
in the relevant screen instead of a crash or silent failure.

---

## Bootstrap Summary

| Environment | Command | Use case |
|-------------|---------|----------|
| Core only | `pip install -r requirements-core.txt` | Daily use, trading, AI chat |
| Core + AI | `pip install -r requirements-core.txt -r requirements-optional-ai.txt` | AI research, LangChain, ML |
| Quant (separate venv) | `pip install -r requirements-optional-quant.txt` | Backtesting, quant modeling |
