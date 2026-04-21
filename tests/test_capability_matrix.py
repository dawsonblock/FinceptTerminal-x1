"""
Capability matrix validation.

Ensures CAPABILITY_MATRIX.md exists and contains the required status
columns for the major feature areas.
Run with: python -m pytest tests/test_capability_matrix.py
"""
import pathlib

REPO = pathlib.Path(__file__).parent.parent
MATRIX = REPO / "CAPABILITY_MATRIX.md"

REQUIRED_FEATURES = [
    "Kalshi",
    "Polymarket",
    "Surface Analytics",
    "Paper Trading",
]

VALID_STATUSES = {"supported", "partial", "experimental", "demo", "planned"}


def test_capability_matrix_exists():
    assert MATRIX.exists(), "CAPABILITY_MATRIX.md is missing"


def test_required_features_listed():
    text = MATRIX.read_text().lower()
    missing = [f for f in REQUIRED_FEATURES if f.lower() not in text]
    assert not missing, f"CAPABILITY_MATRIX.md is missing entries for: {missing}"


def test_status_words_present():
    text = MATRIX.read_text().lower()
    found = [s for s in VALID_STATUSES if s in text]
    assert len(found) >= 3, (
        f"CAPABILITY_MATRIX.md should use status labels from {VALID_STATUSES}; "
        f"only found: {found}"
    )
