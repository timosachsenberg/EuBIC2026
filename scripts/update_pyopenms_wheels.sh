#!/usr/bin/env bash
# Refresh the vendored pyOpenMS nightly wheels in wheels/.
#
# Downloads the latest (or a given) nightly for the Python versions the course
# supports, verifies the SHA256 against the pypi.openms.de index and rewrites
# wheels/SHA256SUMS. The PYOPENMS_VERSION constant in the notebooks' install
# cell still has to be updated by hand afterwards.
#
# Usage: scripts/update_pyopenms_wheels.sh [VERSION]   e.g. 3.6.0.dev20260903
set -euo pipefail

INDEX="https://pypi.openms.de/simple/pyopenms/"
PACKAGES="https://pypi.openms.de/packages"
PLATFORM="manylinux_2_34_x86_64"
PYTAGS=(cp312 cp313)   # cp312 = Google Colab default, cp313 = spare

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
wheel_dir="$repo_root/wheels"
index_html="$(mktemp)"
trap 'rm -f "$index_html"' EXIT

curl -sSfL "$INDEX" -o "$index_html"

version="${1:-}"
if [[ -z "$version" ]]; then
  version="$(grep -oE 'pyopenms-[0-9]+\.[0-9]+\.[0-9]+\.dev[0-9]+' "$index_html" |
             sed 's/^pyopenms-//' | sort -u | tail -1)"
fi
echo "pinning pyopenms $version"

mkdir -p "$wheel_dir"
for tag in "${PYTAGS[@]}"; do
  whl="pyopenms-${version}-${tag}-${tag}-${PLATFORM}.whl"
  expected="$(grep -oE "${whl}#sha256=[0-9a-f]+" "$index_html" | head -1 | cut -d= -f2)"
  if [[ -z "$expected" ]]; then
    echo "  !! $whl is not on the index - skipped" >&2
    continue
  fi
  echo "  downloading $whl"
  curl -sSfL "$PACKAGES/$whl" -o "$wheel_dir/$whl"
  actual="$(sha256sum "$wheel_dir/$whl" | cut -d' ' -f1)"
  if [[ "$actual" != "$expected" ]]; then
    echo "  !! checksum mismatch for $whl" >&2
    rm -f "$wheel_dir/$whl"
    exit 1
  fi
  echo "  checksum ok"
done

( cd "$wheel_dir" && sha256sum ./*.whl | sed 's|\./||' > SHA256SUMS )

echo
echo "Done. Remaining manual steps:"
echo "  1. set PYOPENMS_VERSION = \"$version\" in the install cell of notebooks/*.ipynb"
echo "  2. delete superseded wheels in wheels/ and re-run this script's checksum step"
echo "  3. update the pinned version in wheels/README.md"
