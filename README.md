# Update: Now tracks current pyopenms nightly

# EuBIC2026 Winter School

Educational Jupyter notebooks for the EuBIC 2026 Winter School, teaching proteomics data analysis workflows using PyOpenMS.

## Notebooks

| Notebook | Topic | Description |
|----------|-------|-------------|
| **Task 0** | Prerequisites | Python, NumPy, pandas, and mass spectrometry fundamentals (optional) |
| **Task 1** | Peaks | Protein digestion, MS1 visualization, isotope patterns, TIC |
| **Task 2** | Identification | Peptide database search, fragment spectra, scoring, mirror plots |
| **Task 3** | Quantification | Feature detection with Biosaur2, ID mapping, visualization |

**New to Python or mass spectrometry?** Start with Task 0 to learn the fundamentals.

---

## Quick Start Options

### Option 1: Google Colab (No Installation Required)

The easiest way to run the notebooks is using Google Colab - no local installation needed!

1. Click the **"Open in Colab"** badge at the top of any notebook
2. The notebook will open in your browser
3. Run the first cell to install dependencies (takes ~1-2 minutes)
4. You're ready to go!

**Requirements:** Only a Google account and internet connection.

The install cell pulls a **pinned pyOpenMS nightly wheel that is committed to this
repository** under [`wheels/`](wheels/), fetched from an immutable git tag and verified
by sha256, so every participant gets byte-identical software and the notebooks keep
working even if the nightly build server `pypi.openms.de` is down. If the pinned wheel
does not fit the runtime, the cell falls back to `pypi.openms.de` and then to the stable
PyPI release. See [Updating the pinned pyOpenMS nightly](#updating-the-pinned-pyopenms-nightly).

---

### Option 2: Run Locally on Your Computer

For a better experience or offline work, install the notebooks locally.

#### Prerequisites

- **Python 3.8 or higher** (Python 3.10+ recommended)
- **pip** package manager (comes with Python)
- **Git** (optional, for cloning the repository)

#### Step 1: Download the Repository

**Option A: Using Git (recommended)**
```bash
git clone https://github.com/timosachsenberg/PyOpenMSCourse.git
cd PyOpenMSCourse
```

**Option B: Download ZIP**
1. Go to https://github.com/timosachsenberg/PyOpenMSCourse
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file and navigate to the folder

#### Step 2: Create a Virtual Environment (Recommended)

Using a virtual environment isolates the project dependencies and avoids conflicts with other Python projects.

**On Windows (Command Prompt):**
```bash
python -m venv eubic_env
eubic_env\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
python -m venv eubic_env
.\eubic_env\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv eubic_env
source eubic_env/bin/activate
```

You should see `(eubic_env)` at the beginning of your command prompt, indicating the virtual environment is active.

#### Step 3: Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs:
- `jupyter` / `jupyterlab` - Interactive notebook environment
- `numpy` / `pandas` / `scipy` - Scientific computing
- `matplotlib` / `seaborn` / `plotly` - Visualization
- `pyopenms` (>=3.5.0) - Mass spectrometry data processing
- `pyopenms-viz` (>=1.0.0) - MS-specific visualizations

**Note:** The `pyopenms` installation may take a few minutes as it includes C++ bindings.

**Want the exact build used in the course?** The notebooks pin a pyOpenMS nightly.
On Linux x86_64 you can install the same wheel from this repository:

```bash
pip install wheels/pyopenms-*-cp312-cp312-manylinux_2_34_x86_64.whl
```

(Wheels for CPython 3.11 and 3.13 are vendored as well - swap the `cp312` tag.)

#### Step 4: Start Jupyter

**Option A: JupyterLab (Recommended)**
```bash
jupyter lab
```

**Option B: Classic Jupyter Notebook**
```bash
jupyter notebook
```

Your default web browser will open automatically with the Jupyter interface.

#### Step 5: Open a Notebook

1. In Jupyter, navigate to the `notebooks/` folder
2. Click on a notebook file (e.g., `EUBIC_Task1_Peaks.ipynb`)
3. Run cells with `Shift + Enter` or the "Run" button

---

### Option 3: Using Conda/Miniconda

If you prefer conda for package management:

```bash
# Create a new conda environment
conda create -n eubic2026 python=3.10
conda activate eubic2026

# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter lab
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Command not found: python" or "python is not recognized"

**Cause:** Python is not installed or not in your PATH.

**Solution:**
- Download Python from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart your terminal after installation

#### 2. "ModuleNotFoundError: No module named 'pyopenms'"

**Cause:** Dependencies not installed or wrong Python environment.

**Solution:**
```bash
# Make sure your virtual environment is activated, then:
pip install pyopenms>=3.5.0
```

#### 3. Jupyter kernel dies or notebook won't start

**Cause:** Often a memory issue with large data files.

**Solution:**
- Close other applications to free memory
- Restart Jupyter and try again
- Use smaller data subsets if available

#### 4. Plots not displaying in Jupyter

**Cause:** Plotly renderer not configured.

**Solution:** Add this to the first cell of your notebook:
```python
import plotly.io as pio
pio.renderers.default = "notebook"  # or "jupyterlab" for JupyterLab
```

#### 5. Virtual environment not showing in Jupyter

**Cause:** ipykernel not installed or kernel not registered.

**Solution:**
```bash
# With your virtual environment activated:
pip install ipykernel
python -m ipykernel install --user --name=eubic2026 --display-name="EuBIC 2026"
```

Then restart Jupyter and select "EuBIC 2026" from Kernel > Change Kernel.

#### 6. Permission denied errors on Windows

**Cause:** PowerShell execution policy.

**Solution:** Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 7. SSL/Certificate errors when downloading data

**Cause:** Network/firewall issues.

**Solution:**
- Check your internet connection
- Try a different network
- Download data files manually from the `data/` folder in the repository

---

## Platform-Specific Notes

### Windows
- Use **Command Prompt** or **PowerShell** (not Git Bash for virtual environments)
- Python may be called `python` or `py` depending on installation
- If you have multiple Python versions, use `py -3.10` to specify the version

### macOS
- Use `python3` instead of `python` (macOS includes Python 2 by default)
- You may need to install Xcode Command Line Tools: `xcode-select --install`
- If using Apple Silicon (M1/M2/M3), pyopenms works natively

### Linux
- Use `python3` and `pip3` to ensure you're using Python 3
- You may need to install `python3-venv`: `sudo apt install python3-venv`
- Some distributions require `python3-dev` for building packages

---

## Repository Structure

```
PyOpenMSCourse/
├── notebooks/
│   ├── EUBIC_Task0_Prerequisites.ipynb  # Python & MS fundamentals
│   ├── EUBIC_Task1_Peaks.ipynb          # Digestion & MS1 data
│   ├── EUBIC_Task2_ID.ipynb             # Peptide identification
│   └── EUBIC_Task3_Quant.ipynb          # Quantification
├── data/                                 # Sample data files
├── wheels/                               # Pinned pyOpenMS nightly wheels (Colab fallback)
├── scripts/
│   └── update_pyopenms_wheels.py         # Re-pin / verify the pinned nightly
├── requirements.txt                      # Python dependencies
├── CLAUDE.md                            # AI assistant instructions
└── README.md                            # This file
```

## Data Files

| File | Size | Description | Used by |
|------|------|-------------|---------|
| `UPS1_5min.mzML` | 36 MB | 5-minute RT subset of UPS1 spike-in LC-MS data | Task 1, Task 2, Task 3 |
| `UPS1_5min.idXML` | 14 KB | Peptide identifications for UPS1_5min.mzML | Task 3 |
| `two_ups_proteins.fasta` | 3 KB | 2 UPS1 proteins (Complement C5, EGF) | Task 1, Task 2 |

**Note:** Data files are automatically downloaded when running the notebooks. No manual download required.

---

## Updating the pinned pyOpenMS nightly

The notebooks do **not** install pyOpenMS from `pypi.openms.de` at runtime. They install a
specific nightly wheel that lives in [`wheels/`](wheels/) and is fetched from an immutable
git tag, with the sha256 checked by pip. That gives three things: the course survives an
outage of the nightly server, every participant runs byte-identical software, and a
re-pin is a reviewable diff rather than "whatever was built that morning".

### How the pin is expressed

The install cell at the top of every notebook holds the whole pin:

```python
PYOPENMS_VERSION = "3.6.0.dev20260903"
WHEEL_PIN_REVISION = 2   # bump when the wheel set changes for an unchanged version
WHEEL_REPO = "timosachsenberg/PyOpenMSCourse"
WHEEL_REF = f"wheels-{PYOPENMS_VERSION}-r{WHEEL_PIN_REVISION}"   # git tag holding these wheels
WHEEL_SHA256 = {"cp311": "25c9f994...", "cp312": "b1d8f495...", "cp313": "5772a06e..."}
```

The tag name is derived from the version and the pin revision, so the script has only these
few values to keep in sync. Wheels are built for Linux x86_64 / `manylinux_2_34`, for
CPython 3.11, 3.12 (Google Colab's current runtime) and 3.13, so the pin survives Colab
moving its runtime in either direction.

**Why a pin revision?** Published tags are never moved, so anything that changes the wheel
*set* without changing the pyOpenMS version - adding a Python version, say - needs a new
tag. That is what the revision is for; the script bumps it automatically when it notices
the wheel set changed, and resets it to 1 for a new version. (`wheels-3.6.0.dev20260903`,
without a revision suffix, was the first pin of that version and remains valid.)

### Re-pinning

Do not edit the notebooks by hand - the script rewrites all four consistently, so they can
never drift apart:

```bash
python scripts/update_pyopenms_wheels.py                    # pin the latest nightly
python scripts/update_pyopenms_wheels.py 3.6.0.dev20260903  # or pin a specific one
```

It downloads the wheels, verifies them against the checksums published by the nightly
index, deletes superseded wheels, rewrites `wheels/SHA256SUMS`, and updates
`PYOPENMS_VERSION` and `WHEEL_SHA256` in every notebook.

Then review `git diff`, and publish - **the tag is what the notebooks point at, so pushing
it is not optional**:

```bash
git add wheels notebooks && git commit -m "Pin pyOpenMS 3.6.0.dev20260903"
git push origin main
git tag wheels-3.6.0.dev20260903-r2
git push origin wheels-3.6.0.dev20260903-r2
```

The script prints the exact tag name to use. Never move or delete a published `wheels-*`
tag: older notebook revisions still resolve against it. To change the pin, make a new one.

Adding another Python version is a one-line change to `PY_TAGS` in the script followed by a
re-pin. Each wheel is ~41 MB and stays in git history forever, so add them deliberately.

### Verifying

```bash
python scripts/update_pyopenms_wheels.py --verify
```

This reads the pin out of the notebooks, downloads each pinned URL and compares the served
bytes against the pinned sha256. Run it after pushing the tag, and again shortly before a
course - it is the one check that catches a forgotten `git push --tags`, a moved tag, or
notebooks that disagree with each other. Finally, update the version quoted above and in
[`wheels/README.md`](wheels/README.md).

If the pinned wheel is ever unreachable the notebooks still work: they fall back to
`pypi.openms.de` and then to the stable PyPI release, just without the version guarantee.

---

## Learning Path

1. **Start here:** Run notebooks in order (Task 0 → Task 1 → Task 2 → Task 3)
2. **Each notebook includes:**
   - Collapsible "Deep Dive" sections for advanced concepts
   - "Quick Check" exercises to test understanding
   - pyOpenMS reference tables with documentation links
   - Bonus challenges for further exploration
3. **Estimated time:** 2-3 hours per notebook

---

## Getting Help

- **pyOpenMS Documentation:** https://pyopenms.readthedocs.io/
- **Jupyter Documentation:** https://jupyter.org/documentation
- **Course Issues:** Open an issue on this repository

---

## License

See [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [OpenMS](https://www.openms.de/) - Open-source software for mass spectrometry
- [EuBIC](https://eubic-ms.org/) - European Bioinformatics Community
- [pyopenms-viz](https://pyopenms-viz.readthedocs.io/) - Visualization library

---

*Last updated: January 2026*
