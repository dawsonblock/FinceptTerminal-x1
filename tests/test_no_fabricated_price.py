"""
No-fabrication rule for paper trading.

This test verifies that UnifiedTrading.cpp does NOT contain any code path
that assigns the magic constant 1000.0 as a fill price for market orders.
Instead, it must require a caller-supplied market_price.

Run with:  python -m pytest tests/test_no_fabricated_price.py
"""
import re
import pathlib

REPO = pathlib.Path(__file__).parent.parent
SOURCE = REPO / "fincept-qt" / "src" / "trading" / "UnifiedTrading.cpp"

def test_no_magic_1000_fill():
    text = SOURCE.read_text()
    # Find lines that set price_opt or fill_price to 1000.0
    fabrication = re.findall(r"(?:price_opt|fill_price)\s*=\s*1000\.0", text)
    assert not fabrication, (
        f"Found {len(fabrication)} fabricated fill-price assignment(s) in UnifiedTrading.cpp. "
        "Paper market orders must use caller-supplied market_price, not a magic constant."
    )

def test_market_price_field_in_header():
    """market_price must be declared as a field inside the UnifiedOrder struct in TradingTypes.h."""
    types_h = (REPO / "fincept-qt" / "src" / "trading" / "TradingTypes.h").read_text()
    # Find the UnifiedOrder struct block and verify market_price appears inside it
    struct_match = re.search(r"struct\s+UnifiedOrder\s*\{([^}]*)\}", types_h, re.DOTALL)
    assert struct_match, "UnifiedOrder struct not found in TradingTypes.h"
    struct_body = struct_match.group(1)
    assert "market_price" in struct_body, (
        "UnifiedOrder struct in TradingTypes.h must contain a 'market_price' field "
        "so callers can supply a real quote before paper-trading a market order."
    )

def test_rejection_message_present():
    """UnifiedTrading.cpp must contain the specific rejection string for missing market_price."""
    text = SOURCE.read_text()
    assert "market_price must be supplied" in text, (
        "UnifiedTrading.cpp must contain the explicit rejection message "
        "'market_price must be supplied' when market_price is missing. "
        "Found only partial or no matching text — the no-fabrication contract is not enforced."
    )


# ── CryptoTradingScreen paper-fill guard ─────────────────────────────────────

CRYPTO_SOURCE = REPO / "fincept-qt" / "src" / "screens" / "crypto_trading" / "CryptoTradingScreen.cpp"


def test_crypto_no_magic_1000_fallback():
    """CryptoTradingScreen.cpp must not fabricate a fill price from 1000.0."""
    text = CRYPTO_SOURCE.read_text()
    fabrication = re.findall(r":\s*1000\.0", text)
    assert not fabrication, (
        f"Found {len(fabrication)} magic-constant ternary fallback(s) using 1000.0 in "
        "CryptoTradingScreen.cpp. Paper fills must never invent a price."
    )


def test_crypto_no_value_or_fabrication():
    """CryptoTradingScreen.cpp must not use value_or(1000.0) or any other magic fill constant."""
    text = CRYPTO_SOURCE.read_text()
    fabrication = re.findall(r"value_or\s*\(\s*1000\.0\s*\)", text)
    assert not fabrication, (
        f"Found {len(fabrication)} value_or(1000.0) fabricated fill(s) in CryptoTradingScreen.cpp. "
        "Paper market orders must reject when no valid quote is available."
    )


def test_crypto_market_order_rejects_without_quote():
    """CryptoTradingScreen.cpp must throw/reject a paper market order when ticker.last <= 0."""
    text = CRYPTO_SOURCE.read_text()
    assert "ticker.last <= 0" in text or "ticker.last > 0" in text, (
        "CryptoTradingScreen.cpp must explicitly guard the paper market order path "
        "against a missing or zero quote."
    )
    # The guard must result in an error/rejection, not a fallback price.
    # Confirm that a rejection message mentioning 'price snapshot' is present.
    assert "price snapshot" in text, (
        "CryptoTradingScreen.cpp must surface a clear rejection message when no live "
        "price snapshot is available for a paper market order."
    )
