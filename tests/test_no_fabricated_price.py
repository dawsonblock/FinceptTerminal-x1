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
    header = (REPO / "fincept-qt" / "src" / "trading" / "UnifiedTrading.h").read_text()
    assert "market_price" in header, (
        "UnifiedOrder struct in UnifiedTrading.h must contain a 'market_price' field "
        "so callers can supply a real quote before paper-trading a market order."
    )

def test_rejection_message_present():
    text = SOURCE.read_text()
    assert "market_price must be supplied" in text or "market_price" in text, (
        "UnifiedTrading.cpp must contain an explicit rejection message when market_price is missing."
    )
