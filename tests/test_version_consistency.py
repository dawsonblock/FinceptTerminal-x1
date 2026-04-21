"""
Automated version-consistency check.

Reads VERSION (the single source of truth) and verifies that every
known file that embeds the product version string matches it.
Run with:  python -m pytest tests/test_version_consistency.py
"""
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
    stale_patterns = [f"{major}.{minor}.{p}" for p in range(patch) if f"{major}.{minor}.{p}" != v]

    stale = set()
    # Escape the version specifier separator chars so they don't match in pip pins
    pin_sep = re.compile(r"[><=!]+\s*\d+\.\d+\.\d+")

    for pattern in stale_patterns:
        for ext in ("*.cpp", "*.h", "*.md", "*.json", "*.sh"):
            for p in REPO.rglob(ext):
                # skip git internals
                if ".git" in str(p):
                    continue
                try:
                    text = p.read_text(errors="replace")
                except Exception:
                    continue
                for lineno, line in enumerate(text.splitlines(), 1):
                    if re.search(rf"\b{re.escape(pattern)}\b", line):
                        # Exclude pip requirement pins like `>=4.0.0` or `==4.0.1`
                        if pin_sep.search(line):
                            continue
                        # Exclude URLs with library releases
                        if "pypi" in line.lower() or "pip" in line.lower():
                            continue
                        # Exclude changelog/audit entries recording version transitions
                        if "\u2192" in line:
                            continue
                        stale.add(f"{p.relative_to(REPO)}:{lineno}: {line.strip()}")
    assert not stale, "Stale version strings found:\n" + "\n".join(sorted(stale))
