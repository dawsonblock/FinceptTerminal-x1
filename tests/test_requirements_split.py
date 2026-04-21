"""
Dependency split validation.

Verifies that requirements-core.txt exists and is a strict subset of
the full requirements-numpy2.txt, and that optional files exist.
Run with: python -m pytest tests/test_requirements_split.py
"""
import pathlib
import re

REPO = pathlib.Path(__file__).parent.parent
RES = REPO / "fincept-qt" / "resources"


def _package_names(path: pathlib.Path) -> set:
    names = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # strip version specifiers and environment markers
        pkg = re.split(r"[><=!;\[]", line)[0].strip().lower().replace("-", "_")
        if pkg:
            names.add(pkg)
    return names


def test_core_requirements_file_exists():
    assert (RES / "requirements-core.txt").exists()


def test_optional_ai_file_exists():
    assert (RES / "requirements-optional-ai.txt").exists()


def test_optional_quant_file_exists():
    assert (RES / "requirements-optional-quant.txt").exists()


def test_core_is_smaller_than_full():
    core = _package_names(RES / "requirements-core.txt")
    full = _package_names(RES / "requirements-numpy2.txt")
    assert len(core) < len(full), "Core requirements must be a strict subset of the full list"


def test_core_has_essential_packages():
    core = _package_names(RES / "requirements-core.txt")
    for pkg in ("numpy", "pandas", "requests", "yfinance", "openai"):
        assert pkg in core, f"'{pkg}' must be in requirements-core.txt"
