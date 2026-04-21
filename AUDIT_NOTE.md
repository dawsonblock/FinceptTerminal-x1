# Fincept Terminal — Repair Audit Note
**Version: 4.0.2** | Repair cycle: 4.0.2-hardening

---

## Files Changed

### Version unification
- `VERSION` — created (authoritative version source)
- `fincept-qt/src/mcp/tools/SystemTools.cpp` — 4.0.0 → 4.0.2
- `fincept-qt/src/services/quantlib/QuantLibClient.cpp` — User-Agent 4.0.0 → 4.0.2
- `fincept-qt/src/screens/docs/DocsScreen.cpp` — 4.0.0 → 4.0.2 (2 sites)
- `fincept-qt/src/screens/chat_mode/TerminalToolBridge.cpp` — 4.0.0 → 4.0.2
- `fincept-qt/src/screens/dashboard/DashboardStatusBar.cpp` — 4.0.0 → 4.0.2
- `updates.json` — 4.0.1 → 4.0.2
- `setup.sh` — v4.0.1 → v4.0.2
- `docs/ARCHITECTURE.md` — Version 4.0.1 → 4.0.2
- `docs/CONTRIBUTING.md` — Version 4.0.1 → 4.0.2

### Fabricated price removal
- `fincept-qt/src/trading/UnifiedTrading.cpp` — removed all `1000.0` magic-constant fill prices; market orders now require `market_price > 0` or are rejected
- `fincept-qt/src/trading/TradingTypes.h` — added `market_price` field to `UnifiedOrder`

### Feature fencing
- `fincept-qt/src/screens/surface_analytics/SurfaceAnalyticsScreen.cpp` — `load_demo_data()` clearly marked as demo
- `fincept-qt/src/services/prediction/kalshi/KalshiWsClient.cpp` — stub labeled EXPERIMENTAL with LOG_WARN
- `fincept-qt/src/services/prediction/polymarket/PolymarketAdapter.cpp` — PARTIAL label at top of file

### Dependency split
- `fincept-qt/resources/requirements-core.txt` — created (Tier 1, ~35 packages)
- `fincept-qt/resources/requirements-optional-ai.txt` — created (Tier 2, AI/ML extras)
- `fincept-qt/resources/requirements-optional-quant.txt` — created (Tier 3, quant/backtest extras)

### Tests added
- `tests/__init__.py`
- `tests/test_version_consistency.py`
- `tests/test_no_fabricated_price.py`
- `tests/test_requirements_split.py`
- `tests/test_capability_matrix.py`

### Documents created
- `VERSION`
- `RELEASE_TRUTH.md`
- `CAPABILITY_MATRIX.md`
- `DEPENDENCY_TIERS.md`
- `TEST_PLAN.md`
- `AUDIT_NOTE.md` (this file)

---

## Risks Removed

1. **Version confusion** — users, CI, and user-agent strings all report 4.0.2 consistently
2. **Fabricated paper fills** — no market order can ever receive a made-up `1000.0` price
3. **Silent demo leakage** — Surface Analytics, Kalshi stub, Polymarket partial are clearly labeled
4. **Dependency explosion** — core install is ~35 packages vs 165+ previously; optional packs fail gracefully

---

## Remaining Known Limitations

1. **C++ unit test suite is absent** — adding Qt-based unit tests requires a full Qt build environment; not feasible without CI/CD setup
2. **Kalshi WebSocket live feed** — still a stub; scheduled for Phase 7
3. **Polymarket order lifecycle** — partial; only read paths partially work
4. **Broker test coverage** — Fyers/Motilal adapters lack automated integration tests
5. **PythonRunner graceful-degradation contract** — pattern documented but not mechanically enforced at every call site; callers should be audited
6. **root package.json** — still empty (`{}`); safe to delete but out of scope unless confirmed unused
7. **NumPy 1.x env incompatibility** — quant pack requires a separate venv; C++ app must know which env to invoke (currently assumes single Python path)

---

## What still blocks calling this a true release candidate

- [ ] Automated C++ build + Qt unit tests in CI
- [ ] Integration tests for at least one live broker (mock/recording)
- [ ] Kalshi WebSocket live feed implemented (Phase 7)
- [ ] Polymarket order placement hardened
- [ ] PythonRunner graceful-degradation audit at all call sites
- [ ] SHA-256 hashes populated in `updates.json` for each platform binary
- [ ] SBOM (Software Bill of Materials) for the C++ Qt dependencies
