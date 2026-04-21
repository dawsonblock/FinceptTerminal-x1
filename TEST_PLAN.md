# Fincept Terminal — Test Plan
**Version: 4.0.2**

This document lists the truth-critical automated tests added in the
4.0.2 repair cycle and what each one proves.

---

## How to run all tests

```bash
cd /path/to/FinceptTerminal-x1
python -m pytest tests/ -v
```

No external network access is required. No live broker credentials are required.

---

## Test files

### `tests/test_version_consistency.py`

**What it proves:** Every file that embeds the product version string
contains exactly the authoritative version (read from `VERSION`).

| Test | Assertion |
|------|-----------|
| `test_version_file_exists` | `VERSION` file is present |
| `test_cmake_version` | `CMakeLists.txt` declares the canonical version |
| `test_readme_version` | `README.md` references `v{VERSION}` |
| `test_updates_json_version` | All platforms in `updates.json` match `VERSION` |
| `test_setup_sh_version` | `setup.sh` banner references `v{VERSION}` |
| `test_status_bar_version` | `StatusBar.cpp` displays `v{VERSION}` |
| `test_main_cpp_version` | `main.cpp` logs `v{VERSION}` on startup |
| `test_no_stale_version_040x` | No source/doc file contains a stale earlier 4.0.x product version |

---

### `tests/test_no_fabricated_price.py`

**What it proves:** The paper trading engine can never fabricate a fill
price from the magic constant `1000.0`. Market orders must supply a
caller-provided `market_price`.

| Test | Assertion |
|------|-----------|
| `test_no_magic_1000_fill` | `UnifiedTrading.cpp` contains no `price_opt = 1000.0` or `fill_price = 1000.0` assignments |
| `test_market_price_field_in_header` | `UnifiedTrading.h` contains a `market_price` field in `UnifiedOrder` |
| `test_rejection_message_present` | `UnifiedTrading.cpp` contains the rejection message for missing `market_price` |

---

### `tests/test_requirements_split.py`

**What it proves:** The Python dependency surface is split into core
and optional tiers, and the core tier is meaningfully smaller than
the full requirements list.

| Test | Assertion |
|------|-----------|
| `test_core_requirements_file_exists` | `requirements-core.txt` is present |
| `test_optional_ai_file_exists` | `requirements-optional-ai.txt` is present |
| `test_optional_quant_file_exists` | `requirements-optional-quant.txt` is present |
| `test_core_is_smaller_than_full` | Core package count < full package count |
| `test_core_has_essential_packages` | Core includes numpy, pandas, requests, yfinance, openai |

---

### `tests/test_capability_matrix.py`

**What it proves:** The capability matrix document exists and contains
the required feature entries and status labels.

| Test | Assertion |
|------|-----------|
| `test_capability_matrix_exists` | `CAPABILITY_MATRIX.md` is present |
| `test_required_features_listed` | Kalshi, Polymarket, Surface Analytics, Paper Trading are listed |
| `test_status_words_present` | At least 3 valid status labels appear in the matrix |

---

## Smoke checklist (manual)

These are not automated but must pass before any release:

- [ ] App launches without live broker credentials
- [ ] Paper trading session can be created (init_session → paper mode)
- [ ] Market order with `market_price = 0` returns error, not a fill
- [ ] Market order with valid `market_price` creates a paper fill
- [ ] Surface Analytics screen clearly shows "[DEMO]" label
- [ ] Kalshi screen shows experimental/unavailable notice
- [ ] Polymarket screen shows partial/experimental notice
- [ ] `pip install -r requirements-core.txt` completes without error
- [ ] Core features (market data, news, AI chat) work with only core pack

---

## What is NOT tested (known gaps)

- Full C++ unit tests require a Qt build environment (not run in CI here)
- Live broker order flow (requires real credentials)
- Kalshi/Polymarket live connectivity (stubs; future phase)
- RL agent training/inference
- Full backtesting pipeline (requires NumPy 1.x env)
