# Honesty Audit — Second Pass
**Version: 4.0.2** | Audit date: 2026-04-21

This document records every hit found during the second-pass search for
`demo`, `stub`, `placeholder`, `TODO`, `FIXME`, `hardcoded fallback`,
`deferred`, `unsupported`, and `future phase` across the entire repository,
classified by severity, and showing the resolution applied to each
non-harmless finding.

---

## Classification key

| Class | Meaning |
|-------|---------|
| **release-blocker** | Produces or exposes fabricated/misleading output in a user-reachable path |
| **user-visible risk** | Degrades or misleads user experience; not immediately dangerous but must be disclosed |
| **harmless** | Internal developer note with no user-visible effect |
| **dead code** | Unreachable or overridden by a full implementation |

---

## Findings table

### C++ source (`fincept-qt/src/`)

| # | File | Line(s) | Pattern | Class | Resolution |
|---|------|---------|---------|-------|------------|
| 1 | `trading/brokers/GlobalBrokers.cpp` | 979–1007 | `IMPL_STUB_METHODS` macro returns `"TODO"` as the error string for IBKR, Tradier, SaxoBank order/account operations | **release-blocker** | **PATCHED** — replaced `"TODO"` with `#CLASS ": <method> not implemented in this release"` using C preprocessor stringification |
| 2 | `trading/brokers/IndianBrokers.cpp` | 445–473 | Same `IMPL_STUB_METHODS` macro returning `"TODO"` for Upstox, Dhan, Kotak, AliceBlue, 5Paisa, IIFL, Shoonya order/account operations | **release-blocker** | **PATCHED** — replaced `"TODO"` with `QString("%1: <method> not implemented in this release").arg(name())` |
| 3 | `trading/brokers/IndianBrokers.cpp` | 546 | `IMPL_STUB_METHODS(MotilalBroker)` — appears to duplicate the full implementation in `brokers/motilal/MotilalBroker.cpp` | **dead code** | Left as-is. The full implementation in `motilal/MotilalBroker.cpp` takes precedence at link time. No user-visible effect. Noted in remaining limitations. |
| 4 | `screens/dashboard/widgets/PortfolioSummaryWidget.cpp` | 15–18, 144–148 | Hardcoded `kDemoHoldings` fallback — when a new user has no portfolio, the Dashboard Portfolio Summary widget silently displays six fake holdings (AAPL, MSFT, NVDA, GOOGL, TSLA, SPY) with fabricated share counts | **release-blocker** | **PATCHED** — removed `kDemoHoldings` array; replaced fallback branch with `set_error("No portfolio found. Create a portfolio in the Portfolio screen to track your holdings here.")`. Updated header doc comment. |
| 5 | `screens/markets/MarketPanel.cpp` | 363 | `// TODO: wire volume from API response` — VOL column already shows `"--"` honestly | **harmless** | **PATCHED** — converted to non-TODO comment: `// volume not yet wired from API response` |
| 6 | `storage/secure/SecureStorage.cpp` | 112 | `// TODO: Add libsecret backend for proper encryption on Linux` | **user-visible risk** | **PATCHED** — converted to `// KNOWN LIMITATION (Linux)` comment that accurately describes the security posture without suggesting it will be trivially fixed |
| 7 | `services/prediction/kalshi/KalshiWsClient.cpp` | 62, 87–97 | "Phase 4 keeps this a stub… Phase 7 will enable streaming"; `Subscribe deferred — no credentials configured` | **user-visible risk** | Already patched in Phase 1 (LOG_WARN EXPERIMENTAL notice added). CI test added. |
| 8 | `services/prediction/polymarket/PolymarketAdapter.cpp` | 1–5, 175–179 | `stub_unsupported()` emits error signal for unimplemented paths | **user-visible risk** | Already patched in Phase 1 (PARTIAL/EXPERIMENTAL file header added). |
| 9 | `screens/surface_analytics/SurfaceAnalyticsScreen.cpp` | 344+ | `load_demo_data()` populates surface with synthetic values | **user-visible risk** | Already patched in Phase 1 (DEMO DATA comment added). CI test added. |
| 10 | `trading/AccountDataStream.cpp` | 551–554 | AngelOne WebSocket initialisation "deferred to Phase 5 — ws_ stays null and polling is used" | **harmless** | Polling fallback is functionally correct and honest. The comment accurately describes behavior. No patch needed. |
| 11 | `storage/secure/SecureStorage.cpp` | 112 | (see row 6 above) | — | — |
| 12 | `datahub/Producer.h`, `datahub/TopicPolicy.h` | top | "Phase 0 stub" comments on internal DataHub infrastructure | **harmless** | Internal architecture notes; no user-visible effect. |
| 13 | `screens/support/SupportScreen.cpp` | 843–852, 886, 914 | Synthetic `DEMO-001` ticket always injected into support ticket list | **harmless** | The ticket carries an explicit `DEMO` badge in the UI and the detail panel shows "This is a demo ticket." The intent is transparent to users. No patch needed. |
| 14 | `screens/dashboard/widgets/PortfolioSummaryWidget.h` | 15 | Comment "Falls back to a demo portfolio if no DB holdings are found" | **release-blocker** | **PATCHED** alongside row 4 — updated to accurate description. |
| 15 | `screens/dashboard/canvas/PlaceholderOverlay.h`, `DockScreenRouter.cpp` | various | "lightweight placeholder" for lazily-loaded screens | **harmless** | Standard Qt lazy-loading pattern; not synthetic data. |
| 16 | Various `screens/portfolio/views/*.cpp` | various | `make_placeholder(...)` / `QStackedWidget` with page-0 placeholder labels | **harmless** | These are empty-state prompts ("Run optimization to generate results") shown before the user runs an analysis. They do not display fabricated data. |

---

### Python scripts (`fincept-qt/scripts/`)

| # | File | Line | Pattern | Class | Resolution |
|---|------|------|---------|-------|------------|
| 17 | `agno_trading_service.py` | ~261 | `# TODO: Restore positions from state["positions"]` — competition reload silently skips re-hydrating open positions | **user-visible risk** | **PATCHED** — replaced TODO with an explicit `print("[WARNING] Competition …: positions were not restored …", file=sys.stderr)` that describes exactly what state was lost and what is still correct |
| 18 | `exchange/broker_ws_bridge.py` | 320–335 | `_make_stub(name)` creates stub Python modules for `database.auth_db`, `database.token_db`, etc. | **harmless** | This is intentional module isolation for the WebSocket bridge process; it does not fabricate financial data. |
| 19 | `prediction_kalshi.py` | 21, 71–72 | `use_demo: false` default and `_base_url()` switching between demo-api and prod-api | **harmless** | Explicit user-controlled flag routing to Kalshi's official demo environment; not fabricated data. |
| 20 | Strategy files (`scripts/strategies/*.py`) | various | `placeholder`, `TODO`, `demo` in QuantConnect strategy templates | **harmless** | These are standard QuantConnect template algorithms copied as reference strategies. They are not executed by the app's core trading path. |
| 21 | Analytics scripts (`scripts/Analytics/**/*.py`) | various | `TODO`, `placeholder`, `stub` in quant model implementations | **harmless** | These scripts are invoked via PythonRunner only when the user navigates to quant lab features. All partial paths raise exceptions or return empty results rather than fabricating output. |

---

## Summary of patches applied

| File | Change |
|------|--------|
| `fincept-qt/src/trading/brokers/GlobalBrokers.cpp` | `IMPL_STUB_METHODS` macro: `"TODO"` → `#CLASS ": <method> not implemented in this release"` |
| `fincept-qt/src/trading/brokers/IndianBrokers.cpp` | `IMPL_STUB_METHODS` macro: `"TODO"` → `QString("%1: <method> not implemented in this release").arg(name())` |
| `fincept-qt/src/screens/dashboard/widgets/PortfolioSummaryWidget.cpp` | Removed `kDemoHoldings` array and silent demo fallback; replaced with `set_error()` empty-state prompt |
| `fincept-qt/src/screens/dashboard/widgets/PortfolioSummaryWidget.h` | Updated doc comment to accurately describe new behavior |
| `fincept-qt/src/screens/markets/MarketPanel.cpp` | Converted `// TODO: wire volume` to non-TODO comment |
| `fincept-qt/src/storage/secure/SecureStorage.cpp` | Converted `// TODO` to `// KNOWN LIMITATION (Linux)` |
| `fincept-qt/scripts/agno_trading_service.py` | Replaced silent `# TODO` with explicit `[WARNING]` log |
| `tests/test_honesty_ci.py` | **New** — 7 CI tests that enforce all critical honesty rules |

---

## CI enforcement

The file `tests/test_honesty_ci.py` adds 7 automated tests that will **fail the build** if any of the following release-blocker conditions are reintroduced:

| Test | What it blocks |
|------|----------------|
| `test_no_todo_return_in_trading` | Return statements with `"TODO"` string in trading/prediction paths |
| `test_no_demo_holdings_fallback` | Demo-holdings fallback in `PortfolioSummaryWidget` |
| `test_broker_stub_messages_are_descriptive` | Bare `"TODO"` in broker stub `return` statements |
| `test_surface_analytics_demo_label` | Removal of `DEMO DATA` label from synthetic surface data function |
| `test_kalshi_ws_experimental_warning` | Removal of EXPERIMENTAL warning from Kalshi WS stub |
| `test_agno_trading_position_restore_warned` | Silent position-restore skip without warning |
| `test_no_todo_error_strings_in_screens` | Raw `"TODO"` return values in user-facing screen code |

Run all tests with:
```bash
python -m pytest tests/ -v
# Expected: 26 passed
```

---

## Remaining known limitations (not patched — not release-critical)

1. **Linux credential storage** — XOR-obfuscation only; libsecret not implemented. Disclosed via code comment. Low priority unless Linux is a primary shipping target.
2. **AngelOne WebSocket** — stays null; polling fallback is used. Honest and safe; Phase 5 work.
3. **MotilalBroker stub in IndianBrokers.cpp** — dead code shadowed by full implementation in `motilal/MotilalBroker.cpp`. Should be removed to eliminate confusion but causes no runtime harm.
4. **Kalshi WebSocket live streaming** — still a stub (Phase 7). Labeled and CI-tested.
5. **Polymarket order lifecycle** — partial; `stub_unsupported()` returns error. Labeled.
6. **SupportScreen DEMO-001 ticket** — always injected. Clearly labeled with DEMO badge; users are not misled.
7. **Strategy template TODOs** — in QuantConnect-derived strategy files; not in core trading path.
