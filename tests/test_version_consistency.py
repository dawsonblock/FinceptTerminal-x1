"""
Automated version-consistency check.

Reads VERSION (the single source of truth) and verifies that every
known file that embeds the product version string matches it.
Run with:  python -m pytest tests/test_version_consistency.py

Release gate (set FINCEPT_RELEASE=1 in CI):
  test_updates_sha256_populated — fails if any sha256 hash in updates.json is
  empty.  Must pass before cutting a release tag.
"""
import os
import re
import pathlib

REPO = pathlib.Path(__file__).parent.parent

def canonical_version():
    return (REPO / "VERSION").read_text().strip()

def test_version_file_exists():
    assert (REPO / "VERSION").exists(), "VERSION file missing"

def test_cmake_version():
    v = canonical_version()
    text = (REPO / "fincept-qt" / "CMakeLists.txt").read_text()
    assert f"VERSION {v}" in text, f"CMakeLists.txt must declare VERSION {v}"

def test_readme_version():
    v = canonical_version()
    text = (REPO / "README.md").read_text()
    assert f"v{v}" in text, f"README.md must reference v{v}"

def test_updates_json_version():
    import json
    v = canonical_version()
    data = json.loads((REPO / "updates.json").read_text())
    for platform, info in data["updates"].items():
        got = info["latest-version"]
        assert got == v, f"updates.json platform '{platform}' has version '{got}', expected '{v}'"

def test_updates_sha256_populated():
    """
    Release gate: every platform entry in updates.json must have a non-empty
    sha256 hash before the release is cut.

    This test is enforced only when the FINCEPT_RELEASE environment variable
    is set to '1' (e.g., in the GitHub Actions release workflow).  During
    normal PR development the hashes are intentionally empty because build
    artifacts do not exist yet.

    To enable locally:  FINCEPT_RELEASE=1 python -m pytest tests/ -v
    """
    import json
    if os.environ.get("FINCEPT_RELEASE") != "1":
        import pytest
        pytest.skip("sha256 gate is only enforced when FINCEPT_RELEASE=1")
    data = json.loads((REPO / "updates.json").read_text())
    missing = [
        platform
        for platform, info in data["updates"].items()
        if not info.get("sha256", "").strip()
    ]
    assert not missing, (
        f"updates.json has empty sha256 for platform(s): {missing}. "
        "Populate the correct sha256 hashes before publishing this release — "
        "the auto-updater skips integrity verification when the hash is absent."
    )

def test_setup_sh_version():
    v = canonical_version()
    text = (REPO / "setup.sh").read_text()
    assert f"v{v}" in text, f"setup.sh must reference v{v}"

def test_status_bar_version():
    v = canonical_version()
    text = (REPO / "fincept-qt" / "src" / "ui" / "navigation" / "StatusBar.cpp").read_text()
    assert f"v{v}" in text, f"StatusBar.cpp must display v{v}"

def test_main_cpp_version():
    v = canonical_version()
    text = (REPO / "fincept-qt" / "src" / "app" / "main.cpp").read_text()
    assert f"v{v}" in text or f"v{v[:-2]}" in text, f"main.cpp must log v{v}"

def test_no_stale_version_040x():
    """No C++ source or core doc file should contain a different 4.0.x version."""
    v = canonical_version()
    # Parse major/minor to derive which patch versions count as stale.
    # Stale = any 4.0.N where N < current patch number.
    m = re.match(r"(\d+)\.(\d+)\.(\d+)", v)
    assert m, f"Cannot parse canonical version '{v}'"
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    stale_patterns = [
        f"{major}.{minor}.{p}"
        for p in range(patch)
        if f"{major}.{minor}.{p}" != v
    ]

    if not stale_patterns:
        return  # nothing to check (patch is 0)

    # Build a single compiled alternation so each file is read exactly once.
    stale_re = re.compile(
        r"\b(" + "|".join(re.escape(s) for s in stale_patterns) + r")\b"
    )
    # Exclude lines that are pip-style version pins or changelog arrows
    pin_sep = re.compile(r"[><=!]+\s*\d+\.\d+\.\d+")

    stale = set()
    for ext in ("*.cpp", "*.h", "*.md", "*.json", "*.sh"):
        for p in REPO.rglob(ext):
            if ".git" in str(p):
                continue
            try:
                text = p.read_text(errors="replace")
            except Exception:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                if stale_re.search(line):
                    if pin_sep.search(line):
                        continue
                    if "pypi" in line.lower() or "pip" in line.lower():
                        continue
                    if "\u2192" in line:
                        continue
                    stale.add(f"{p.relative_to(REPO)}:{lineno}: {line.strip()}")
    assert not stale, "Stale version strings found:\n" + "\n".join(sorted(stale))
