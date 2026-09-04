# Pinned pyOpenMS nightly wheels

The notebooks install pyOpenMS from a **pinned nightly build committed here**, not from
`pypi.openms.de` at runtime. The wheels are fetched from an immutable git tag and their
sha256 is checked by pip, so the course survives an outage of the nightly build server and
every participant runs byte-identical software.

| | |
|---|---|
| Pinned version | `3.6.0.dev20260903` |
| Git tag | `wheels-3.6.0.dev20260903-r2` |
| Upstream | `https://pypi.openms.de/simple/pyopenms/` |
| Platform | `manylinux_2_34_x86_64` (Linux, glibc ≥ 2.34) |
| Python | CPython 3.11, 3.12 and 3.13 (Google Colab's runtime) |

Checksums are in [`SHA256SUMS`](SHA256SUMS); they match the hashes published by the
pypi.openms.de simple index and the `WHEEL_SHA256` values in the notebooks.

## How the notebooks use it

The install cell resolves the wheel for the running interpreter and tries, in order:

1. `https://raw.githubusercontent.com/<repo>/wheels-<version>-r<revision>/wheels/<wheel>#sha256=...`
2. the nightly index `https://pypi.openms.de/simple/`
3. the stable `pyopenms` release from PyPI

Step 1 is skipped on macOS/Windows and on any Python version without a vendored wheel; the
`#sha256=` fragment makes pip reject the download if the bytes ever differ from the pin.

## Re-pinning and verifying

Both are scripted - do not edit the notebooks by hand:

```bash
python ../scripts/update_pyopenms_wheels.py           # pin the latest nightly
python ../scripts/update_pyopenms_wheels.py --verify  # check the published pin
```

The full procedure, including publishing the git tag the notebooks point at, is in
[Updating the pinned pyOpenMS nightly](../README.md#updating-the-pinned-pyopenms-nightly).
Never move or delete a published `wheels-*` tag; a changed wheel set gets a new pin
revision instead.

## Installing manually

```bash
pip install wheels/pyopenms-3.6.0.dev20260903-cp313-cp313-manylinux_2_34_x86_64.whl
```
