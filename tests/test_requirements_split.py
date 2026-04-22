"""
Dependency split validation.

Verifies that the three documented dependency tier files exist and that the
bootstrap code (PythonSetupManager.cpp) is wired to the real tier files, not
the legacy requirements-numpy1/numpy2 split files.

Run with: python -m pytest tests/test_requirements_split.py
"""
import pathlib
import re

REPO = pathlib.Path(__file__).parent.parent
RES = REPO / "fincept-qt" / "resources"
SETUP_MGR = REPO / "fincept-qt" / "src" / "python" / "PythonSetupManager.cpp"


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


def test_core_has_essential_packages():
    core = _package_names(RES / "requirements-core.txt")
    for pkg in ("numpy", "pandas", "requests", "yfinance", "openai"):
        assert pkg in core, f"'{pkg}' must be in requirements-core.txt"


def test_setup_manager_uses_core_tier_file():
    """PythonSetupManager.cpp must install requirements-core.txt, not requirements-numpy2.txt."""
    text = SETUP_MGR.read_text()
    assert "requirements-core.txt" in text, (
        "PythonSetupManager.cpp must reference requirements-core.txt "
        "to wire the documented Tier-1 install path."
    )
    assert "requirements-numpy2.txt" not in text, (
        "PythonSetupManager.cpp still references requirements-numpy2.txt — "
        "the old legacy split file must not drive the bootstrap. "
        "Wire requirements-core.txt instead (Tier 1)."
    )


def test_setup_manager_uses_quant_tier_file():
    """PythonSetupManager.cpp must install requirements-optional-quant.txt, not requirements-numpy1.txt."""
    text = SETUP_MGR.read_text()
    assert "requirements-optional-quant.txt" in text, (
        "PythonSetupManager.cpp must reference requirements-optional-quant.txt "
        "to wire the documented Tier-3 quant install path."
    )
    assert "requirements-numpy1.txt" not in text, (
        "PythonSetupManager.cpp still references requirements-numpy1.txt — "
        "the old legacy split file must not drive the bootstrap. "
        "Wire requirements-optional-quant.txt instead (Tier 3)."
    )
