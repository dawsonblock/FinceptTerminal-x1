"""
Honesty CI gate — second-pass release safety.

These tests enforce that no release-blocker honesty issue remains in
user-facing code paths.  They are fast, deterministic, and require no
build environment or live credentials.

Run with:  python -m pytest tests/test_honesty_ci.py -v
"""

import re
import pathlib

REPO = pathlib.Path(__file__).parent.parent
SRC = REPO / "fincept-qt" / "src"
SCRIPTS = REPO / "fincept-qt" / "scripts"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _read(path: pathlib.Path) -> str:
    return path.read_text(errors="replace")


# ---------------------------------------------------------------------------
# Rule 1 — no literal "TODO" as a return-value string in trading/broker paths
# ---------------------------------------------------------------------------

def test_no_todo_return_in_trading():
    """
    Broker stub methods must NOT return the raw string "TODO" as an error
    message.  Users who attempt an unsupported operation should receive a
    descriptive 'not implemented' message, not a raw development marker.

    Patterns caught:
      return {false, "", "TODO"};
      return {false, std::nullopt, "TODO", ts};
      return "TODO";
      return make_error("TODO");
    """
    TRADING_DIRS = [
        SRC / "trading",
        SRC / "services" / "prediction",
    ]
    # Matches any return statement that contains the literal string "TODO"
    todo_return = re.compile(r'\breturn\b[^;]*"TODO"[^;]*;')
    hits = []
    for d in TRADING_DIRS:
        for p in d.rglob("*.cpp"):
            for lineno, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
                if todo_return.search(line):
                    hits.append(f"{p.relative_to(REPO)}:{lineno}: {line.strip()}")
    assert not hits, (
        "Found return statements with raw 'TODO' error strings in trading paths "
        "(release blocker — users see 'TODO' as an error message):\n"
        + "\n".join(hits)
    )


# ---------------------------------------------------------------------------
# Rule 2 — PortfolioSummaryWidget must NOT have a demo-holdings fallback
# ---------------------------------------------------------------------------

def test_no_demo_holdings_fallback():
    """
    The dashboard Portfolio Summary widget must not fall back to hardcoded
    demo holdings when no real portfolio exists.  Showing fake portfolio data
    to new users is misleading.
    """
    psw = SRC / "screens" / "dashboard" / "widgets" / "PortfolioSummaryWidget.cpp"
    text = _read(psw)
    # These patterns indicate a demo-holdings silent fallback
    bad_patterns = [
        r"kDemoHoldings",
        r"Fall\s+back\s+to\s+demo\s+portfolio",
        r"holdings\s*=\s*kDemo",
    ]
    for pat in bad_patterns:
        m = re.search(pat, text)
        assert not m, (
            f"PortfolioSummaryWidget.cpp still contains demo-holdings fallback "
            f"(pattern: {pat!r}).  Replace with an empty-state prompt."
        )


# ---------------------------------------------------------------------------
# Rule 3 — no broker stub error message is the single word "TODO"
# ---------------------------------------------------------------------------

def test_broker_stub_messages_are_descriptive():
    """
    All broker stub error messages must NOT be the bare string "TODO".
    Matches any return statement containing "TODO" in either broker file.
    """
    todo_return = re.compile(r'\breturn\b[^;]*"TODO"[^;]*;')
    for fname in ("GlobalBrokers.cpp", "IndianBrokers.cpp"):
        path = SRC / "trading" / "brokers" / fname
        for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if todo_return.search(line):
                assert False, (
                    f"{path.relative_to(REPO)}:{lineno}: broker stub returns bare 'TODO' "
                    f"string: {line.strip()}"
                )


# ---------------------------------------------------------------------------
# Rule 4 — SurfaceAnalyticsScreen must label its demo-data calls
# ---------------------------------------------------------------------------

def test_surface_analytics_demo_label():
    """
    SurfaceAnalyticsScreen::load_demo_data() must carry a DEMO DATA comment
    so the intent is clear to developers and auditors.
    """
    sa = SRC / "screens" / "surface_analytics" / "SurfaceAnalyticsScreen.cpp"
    text = _read(sa)
    assert "DEMO DATA" in text, (
        "SurfaceAnalyticsScreen.cpp must contain a 'DEMO DATA' label inside or "
        "near load_demo_data() to make the synthetic-data intent explicit."
    )


# ---------------------------------------------------------------------------
# Rule 5 — KalshiWsClient must emit a visible warning on its stub path
# ---------------------------------------------------------------------------

def test_kalshi_ws_experimental_warning():
    """
    The Kalshi WebSocket stub must LOG_WARN or otherwise signal that the live
    connection is not yet implemented, so users don't assume streaming works.
    """
    kws = SRC / "services" / "prediction" / "kalshi" / "KalshiWsClient.cpp"
    text = _read(kws)
    assert "EXPERIMENTAL" in text or "not yet implemented" in text, (
        "KalshiWsClient.cpp must contain an EXPERIMENTAL or 'not yet implemented' "
        "label on its stub WebSocket path."
    )


# ---------------------------------------------------------------------------
# Rule 6 — agno_trading_service.py must warn when positions are not restored
# ---------------------------------------------------------------------------

def test_agno_trading_position_restore_warned():
    """
    When competition state is loaded from DB but positions cannot be restored,
    the code must emit a WARNING to stderr rather than silently skipping.
    """
    svc = SCRIPTS / "agno_trading_service.py"
    text = _read(svc)
    # Must NOT contain a silent bare TODO
    assert "# TODO: Restore positions" not in text, (
        "agno_trading_service.py still has a silent TODO for position restore — "
        "it must emit an explicit warning so users know state was lost."
    )
    # Must contain a warning
    assert "WARNING" in text and "positions" in text.lower(), (
        "agno_trading_service.py must emit a WARNING when positions are not "
        "restored from saved competition state."
    )


# ---------------------------------------------------------------------------
# Rule 7 — no file in user-facing C++ screens returns a raw "TODO" error
# ---------------------------------------------------------------------------

def test_no_todo_error_strings_in_screens():
    """
    User-facing screen code must not contain return statements that expose
    bare 'TODO' strings to the UI layer.  Matches all common return forms:
      return {false, "TODO"};
      return "TODO";
      return make_error("TODO");
    """
    screens_dir = SRC / "screens"
    todo_return = re.compile(r'\breturn\b[^;]*"TODO"[^;]*;')
    hits = []
    for p in screens_dir.rglob("*.cpp"):
        for lineno, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            if todo_return.search(line):
                hits.append(f"{p.relative_to(REPO)}:{lineno}: {line.strip()}")
    assert not hits, (
        "Found return statements with raw 'TODO' error strings in screen code:\n"
        + "\n".join(hits)
    )
