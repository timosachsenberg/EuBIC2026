#!/usr/bin/env python3
"""Manage the pinned pyOpenMS nightly wheels vendored in wheels/.

The notebooks install pyOpenMS from a wheel committed to this repository and
served from an immutable git tag, so the course survives an outage of the
nightly build server. This script owns that pin end to end: it downloads the
wheels, verifies them against the pypi.openms.de index, drops superseded ones,
rewrites wheels/SHA256SUMS and rewrites the install cell of every notebook.

    python scripts/update_pyopenms_wheels.py               # pin the latest nightly
    python scripts/update_pyopenms_wheels.py 3.6.0.dev20260903
    python scripts/update_pyopenms_wheels.py --verify      # check the published pin

See "Updating the pinned pyOpenMS nightly" in README.md for the full procedure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

INDEX_URL = "https://pypi.openms.de/simple/pyopenms/"
PACKAGES_URL = "https://pypi.openms.de/packages"
PLATFORM = "manylinux_2_34_x86_64"
PY_TAGS = ("cp312", "cp313")  # cp312 = Google Colab's runtime, cp313 = spare

REPO_ROOT = Path(__file__).resolve().parent.parent
WHEEL_DIR = REPO_ROOT / "wheels"
NOTEBOOK_DIR = REPO_ROOT / "notebooks"

VERSION_RE = re.compile(r'^PYOPENMS_VERSION = "(?P<version>[^"]+)"$', re.MULTILINE)
SHA_BLOCK_RE = re.compile(r"^WHEEL_SHA256 = \{\n(?:.*\n)*?\}$", re.MULTILINE)
SHA_ENTRY_RE = re.compile(r'^\s*"(?P<tag>cp\d+)": "(?P<sha>[0-9a-f]{64})",$', re.MULTILINE)
REPO_RE = re.compile(r'^WHEEL_REPO = "(?P<repo>[^"]+)"$', re.MULTILINE)
REF_RE = re.compile(r'^WHEEL_REF = f"(?P<ref>[^"]*)"', re.MULTILINE)


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def wheel_name(version: str, tag: str) -> str:
    return f"pyopenms-{version}-{tag}-{tag}-{PLATFORM}.whl"


def read_index() -> dict[str, str]:
    """Map wheel filename -> sha256 as published by the nightly index."""
    html = fetch(INDEX_URL).decode()
    return dict(re.findall(r'(pyopenms-[^"#]+\.whl)#sha256=([0-9a-f]{64})', html))


def install_cell(path: Path) -> tuple[dict, str]:
    """Return the install cell of a notebook and its joined source."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "code" and "PYOPENMS_VERSION" in source:
            return notebook, source
    raise SystemExit(f"{path}: no install cell with PYOPENMS_VERSION found")


def pinned_config() -> dict:
    """Read the pin the notebooks currently declare (they must all agree)."""
    configs = {}
    for path in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
        _, source = install_cell(path)
        version = VERSION_RE.search(source)
        repo = REPO_RE.search(source)
        ref = REF_RE.search(source)
        if not (version and repo and ref):
            raise SystemExit(f"{path}: install cell does not match the expected layout")
        configs[path.name] = {
            "version": version["version"],
            "repo": repo["repo"],
            "ref": ref["ref"].replace("{PYOPENMS_VERSION}", version["version"]),
            "sha256": {m["tag"]: m["sha"] for m in SHA_ENTRY_RE.finditer(source)},
        }
    distinct = {json.dumps(c, sort_keys=True) for c in configs.values()}
    if len(distinct) != 1:
        for name, config in configs.items():
            print(f"  {name}: {config}")
        raise SystemExit("notebooks disagree about the pinned wheel - re-run without --verify")
    return next(iter(configs.values()))


def verify() -> int:
    """Check that the pinned URLs really serve the pinned bytes."""
    config = pinned_config()
    base = f"https://raw.githubusercontent.com/{config['repo']}/{config['ref']}/wheels"
    print(f"pinned version : {config['version']}")
    print(f"pinned ref     : {config['ref']}")
    failures = 0

    for tag, expected in sorted(config["sha256"].items()):
        name = wheel_name(config["version"], tag)
        local = WHEEL_DIR / name
        if not local.is_file():
            print(f"  {tag}: MISSING from wheels/ ({name})")
            failures += 1
        elif hashlib.sha256(local.read_bytes()).hexdigest() != expected:
            print(f"  {tag}: local wheel does not match the pinned sha256")
            failures += 1

        try:
            served = hashlib.sha256(fetch(f"{base}/{name}")).hexdigest()
        except urllib.error.URLError as exc:
            print(f"  {tag}: {base}/{name} is not reachable ({exc}) - is the tag pushed?")
            failures += 1
            continue
        if served == expected:
            print(f"  {tag}: ok ({name})")
        else:
            print(f"  {tag}: SERVED BYTES DIFFER (got {served}, pinned {expected})")
            failures += 1

    print("pin verified" if not failures else f"{failures} problem(s) found")
    return 1 if failures else 0


def rewrite_notebooks(version: str, hashes: dict[str, str]) -> None:
    block = "WHEEL_SHA256 = {\n"
    block += "".join(f'    "{tag}": "{hashes[tag]}",\n' for tag in sorted(hashes))
    block += "}"

    for path in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            source = "".join(cell["source"])
            if cell["cell_type"] != "code" or "PYOPENMS_VERSION" not in source:
                continue
            updated = VERSION_RE.sub(f'PYOPENMS_VERSION = "{version}"', source)
            updated, count = SHA_BLOCK_RE.subn(block.replace("\\", "\\\\"), updated)
            if count != 1:
                raise SystemExit(f"{path}: could not locate the WHEEL_SHA256 block")
            if updated == source:
                print(f"  {path.name}: already up to date")
                break
            cell["source"] = [line + "\n" for line in updated.split("\n")[:-1]]
            path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8", newline="")
            print(f"  {path.name}: pinned to {version}")
            break


def update(version: str | None) -> int:
    index = read_index()
    if version is None:
        versions = {re.search(r"pyopenms-([^-]+)-", name)[1] for name in index}
        version = sorted(versions, key=lambda v: re.sub(r"\D", "", v))[-1]
    print(f"pinning pyopenms {version}")

    WHEEL_DIR.mkdir(exist_ok=True)
    hashes: dict[str, str] = {}
    for tag in PY_TAGS:
        name = wheel_name(version, tag)
        expected = index.get(name)
        if expected is None:
            print(f"  {tag}: {name} is not on the index - skipped")
            continue
        target = WHEEL_DIR / name
        if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == expected:
            print(f"  {tag}: already present and verified")
        else:
            print(f"  {tag}: downloading {name}")
            payload = fetch(f"{PACKAGES_URL}/{name}")
            actual = hashlib.sha256(payload).hexdigest()
            if actual != expected:
                raise SystemExit(f"  {tag}: checksum mismatch (got {actual}, index says {expected})")
            target.write_bytes(payload)
            print(f"  {tag}: checksum ok")
        hashes[tag] = expected

    if not hashes:
        raise SystemExit(f"no wheels available for {version}")

    for stale in sorted(WHEEL_DIR.glob("pyopenms-*.whl")):
        if stale.name not in {wheel_name(version, tag) for tag in hashes}:
            stale.unlink()
            print(f"  removed superseded {stale.name}")

    checksums = "".join(
        f"{hashes[tag]}  {wheel_name(version, tag)}\n" for tag in sorted(hashes)
    )
    (WHEEL_DIR / "SHA256SUMS").write_text(checksums, encoding="utf-8", newline="")
    rewrite_notebooks(version, hashes)

    tag_name = f"wheels-{version}"
    print(
        f"\nDone. Commit, then publish the immutable tag the notebooks point at:\n"
        f"  git add wheels notebooks && git commit -m 'Pin pyOpenMS {version}'\n"
        f"  git push origin main\n"
        f"  git tag {tag_name} && git push origin {tag_name}\n"
        f"  python scripts/update_pyopenms_wheels.py --verify\n"
        f"Also refresh the pinned version quoted in README.md and wheels/README.md."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("version", nargs="?",
                        help="nightly to pin, e.g. 3.6.0.dev20260903 (default: latest)")
    parser.add_argument("--verify", action="store_true",
                        help="check that the pinned URLs serve the pinned bytes")
    args = parser.parse_args()
    if args.verify:
        if args.version:
            parser.error("--verify takes no version argument")
        return verify()
    return update(args.version)


if __name__ == "__main__":
    sys.exit(main())
