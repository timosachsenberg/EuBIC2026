# Vendored pyOpenMS nightly wheels

This directory holds a **pinned pyOpenMS nightly build**, committed to the repository
so that the course notebooks keep working even when the nightly build server
<https://pypi.openms.de> is unreachable.

| | |
|---|---|
| Pinned version | `3.6.0.dev20260903` |
| Source | `https://pypi.openms.de/simple/pyopenms/` |
| Platform | `manylinux_2_34_x86_64` (Linux, glibc ≥ 2.34) |
| Python | CPython 3.12 (Google Colab default) and 3.13 (spare) |

Checksums of the committed files are in [`SHA256SUMS`](SHA256SUMS) and match the
hashes published by the pypi.openms.de simple index.

## How the notebooks use it

Every notebook starts with an install cell that tries, in order:

1. the wheel in this directory, fetched over `raw.githubusercontent.com`
   (pinned, works while GitHub is up),
2. the nightly index `https://pypi.openms.de/simple/`,
3. the stable `pyopenms` release from PyPI.

The wheel is selected from the running interpreter, e.g. Python 3.12 on Linux
x86_64 resolves to `pyopenms-3.6.0.dev20260903-cp312-cp312-manylinux_2_34_x86_64.whl`.
On macOS/Windows or a Python version without a vendored wheel, step 1 is skipped
and the notebook falls back to the online sources.

Colab currently runs **Ubuntu 22.04 (glibc 2.35) with Python 3.12** on x86_64, so
the `cp312` wheel is the one that is actually used during the course. The `cp313`
wheel is insurance in case Colab bumps its runtime.

## Refreshing the pin

```bash
# picks the latest nightly, downloads cp312 + cp313, verifies checksums,
# and prints the notebook edit that is still needed
./scripts/update_pyopenms_wheels.sh
```

Then update `PYOPENMS_VERSION` in the install cell of every notebook in
`notebooks/` and delete the superseded `.whl` files, so the repository keeps
exactly one pinned nightly.

## Install manually

```bash
pip install wheels/pyopenms-3.6.0.dev20260903-cp312-cp312-manylinux_2_34_x86_64.whl
```
