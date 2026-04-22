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
- `fincept-qt/src/screens/crypto_trading/CryptoTradingScreen.cpp` — removed `ticker.last > 0 ? ticker.last : 1000.0` and `price_opt.value_or(1000.0)` fabricated fill fallbacks; paper market orders now throw when `ticker.last <= 0` with a clear rejection message

### Feature fencing
- `fincept-qt/src/screens/surface_analytics/SurfaceAnalyticsScreen.cpp` — `load_demo_data()` clearly marked as demo
- `fincept-qt/src/services/prediction/kalshi/KalshiWsClient.cpp` — stub labeled EXPERIMENTAL with LOG_WARN
- `fincept-qt/src/services/prediction/polymarket/PolymarketAdapter.cpp` — PARTIAL label at top of file

### Dependency tier wiring (second pass)
- `fincept-qt/resources/requirements-core.txt` — created (Tier 1, ~35 packages)
- `fincept-qt/resources/requirements-optional-ai.txt` — created (Tier 2, AI/ML extras)
- `fincept-qt/resources/requirements-optional-quant.txt` — created (Tier 3, quant/backtest extras)
- `fincept-qt/src/python/PythonSetupManager.cpp` — wired to `requirements-core.txt` (venv-numpy2) and `requirements-optional-quant.txt` (venv-numpy1); legacy numpy1/numpy2 split files no longer drive bootstrap
- `fincept-qt/src/screens/settings/PythonEnvSection.cpp` — updated to read tier files
- `fincept-qt/src/screens/settings/PythonEnvSection.h` — updated doc comment
- `fincept-qt/src/screens/setup/SetupScreen.cpp` — updated message replacements to use tier names
- `fincept-qt/CMakeLists.txt` — POST_BUILD copies and install rules updated to deploy tier files
- `.github/workflows/release.yml` — AppImage packaging updated to copy tier files

### Tests added / updated
- `tests/__init__.py`
- `tests/test_version_consistency.py`
- `tests/test_no_fabricated_price.py` — new tests for CryptoTradingScreen no-fabrication rule (3 tests added)
- `tests/test_requirements_split.py` — replaced obsolete numpy2 subset check with tier-wiring tests
- `tests/test_capability_matrix.py`

### Documents created / updated
- `VERSION`
- `RELEASE_TRUTH.md`
- `CAPABILITY_MATRIX.md`
- `DEPENDENCY_TIERS.md`
- `TEST_PLAN.md`
- `AUDIT_NOTE.md` (this file)
- `HONESTY_AUDIT.md` — updated with CryptoTradingScreen finding and resolution; updated CI test table

---

## Risks Removed

1. **Version confusion** — users, CI, and user-agent strings all report 4.0.2 consistently
2. **Fabricated paper fills** — no market order in either `UnifiedTrading.cpp` or `CryptoTradingScreen.cpp` can ever receive a made-up price; both paths now reject when no live quote is available
3. **Silent demo leakage** — Surface Analytics, Kalshi stub, Polymarket partial are clearly labeled
4. **Dependency explosion** — core install is ~35 packages vs 165+ previously; optional packs fail gracefully
5. **Bootstrap truth gap** — runtime now installs `requirements-core.txt` and `requirements-optional-quant.txt` matching the documented tier model exactly

---

## Remaining Known Limitations

1. **C++ unit test suite is absent** — adding Qt-based unit tests requires a full Qt build environment; not feasible without CI/CD setup
2. **Kalshi WebSocket live feed** — still a stub; scheduled for Phase 7
3. **Polymarket order lifecycle** — partial; only read paths partially work
4. **Broker test coverage** — Fyers/Motilal adapters lack automated integration tests
5. **PythonRunner graceful-degradation contract** — pattern documented but not mechanically enforced at every call site; callers should be audited
6. **root package.json** — still empty (`{}`); safe to delete but out of scope unless confirmed unused
7. **Optional AI tier not separately venv'd** — `requirements-optional-ai.txt` exists and is documented but the current bootstrap installs only `requirements-core.txt` in venv-numpy2; AI pack install is a manual step. Disclosed in DEPENDENCY_TIERS.md.

---

## What still blocks calling this a true release candidate

- [ ] Automated C++ build + Qt unit tests in CI
- [ ] Integration tests for at least one live broker (mock/recording)
- [ ] Kalshi WebSocket live feed implemented (Phase 7)
- [ ] Polymarket order placement hardened
- [ ] PythonRunner graceful-degradation audit at all call sites
- [ ] SHA-256 hashes populated in `updates.json` for each platform binary
- [ ] SBOM (Software Bill of Materials) for the C++ Qt dependencies
