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
git clone https://github.com/timosachsenberg/EuBIC2026.git
cd EuBIC2026
```

**Option B: Download ZIP**
1. Go to https://github.com/timosachsenberg/EuBIC2026
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
EuBIC2026/
├── notebooks/
│   ├── EUBIC_Task0_Prerequisites.ipynb  # Python & MS fundamentals
│   ├── EUBIC_Task1_Peaks.ipynb          # Digestion & MS1 data
│   ├── EUBIC_Task2_ID.ipynb             # Peptide identification
│   └── EUBIC_Task3_Quant.ipynb          # Quantification
├── data/                                 # Sample data files
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
