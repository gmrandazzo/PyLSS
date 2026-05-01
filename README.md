# PyLSS

PyLSS [1] is a Python package designed to calculate linear solvent strength (LSS) parameters [2] in Liquid Chromatography.

PyLSS features a personalized optimization algorithm that rapidly and accurately calculates LSS parameters, making it an invaluable tool for method development and retention time prediction.

![ScreenShot](https://github.com/gmrandazzo/PyLSS/raw/master/gui/pylssgui.png)

## Features

- **Compute LSS Parameters:** Calculate $\log(k_w)$ and $S$ from experimental data under linear and logarithmic gradient conditions.
- **Chromatogram Simulation:** Build, plot, and export chromatograms from experimental or predicted retention times.
- **Separation Optimization:** Optimize isocratic and gradient conditions automatically using built-in algorithms (e.g., Nelder-Mead simplex).
- **Interactive GUI:** A modern, PyQt6-based graphical user interface to effortlessly manage models, estimate parameters, and visualize results (Selectivity and Resolution maps).
- **Command-Line Tools:** Powerful CLI executables for batch processing and automated workflows.

## Dependencies

The required dependencies to use PyLSS are:

- Python 3.8+
- `numpy`
- `scipy`
- `matplotlib`
- `PyQt6` (for the GUI)

## Installation

It is recommended to install PyLSS within a virtual environment. The project uses a modern `pyproject.toml` build system.

```bash
# Clone the repository
git clone https://github.com/gmrandazzo/PyLSS.git
cd PyLSS

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the package and its dependencies
pip install .
```

## Usage

### Input File Specification

PyLSS uses a standardized `.lss` format that combines experimental metadata (YAML) and retention data (CSV).

#### Format Structure
```yaml
---
# Mandatory: System Parameters
t0: 0.969            # Column dead time (min)
dwell_volume: 0.375  # System dwell volume (mL)
flow_rate: 0.30      # Flow rate (mL/min)

# Mandatory: Gradient Definitions
# Each list item is: [Gradient Time (min), %B Start, %B End]
gradients:
  - [14, 5, 95]
  - [60, 5, 95]

# Optional: Column Metadata
column_length: 15.0   # cm
column_diameter: 2.1  # mm
column_particle: 1.7  # µm
---
# Retention Data (CSV section)
# Format: Molecule Name; Tr (Grad 1); Tr (Grad 2); ...
Steroid_A; 8.53; 22.11
Steroid_B; 9.07; 24.54
```

**Key Rules:**
1. **Metadata Section:** Must be enclosed between triple dashes (`---`).
2. **Mandatory Fields:** `t0`, `dwell_volume`, `flow_rate`, and `gradients`.
3. **Data Delimiter:** The parser automatically detects semicolons (`;`), commas (`,`), or tabs. Semicolons are recommended.
4. **Molecule Names:** If the first column contains text, it is used as the name. If it's numeric, a name is auto-generated.

### Graphical User Interface (GUI)

Once installed, you can launch the interactive GUI directly from your terminal:

```bash
pylss-gui
```

You can also launch the standalone Chromatogram Analyzer:

```bash
pylss-chromanalyzer
```

### Command Line Tools (CLI)

Installing PyLSS automatically registers several command-line tools in your environment. You can run these from anywhere:

- `pylss-lssgen`: Calculate $\log(k_w)$ and $S$ parameters from an input file.
- `pylss-lssopt`: Optimize separation conditions based on LSS parameters.
- `pylss-logssgen`: Generate logarithmic solvent strength parameters.
- `pylss-logssopt`: Optimize logarithmic gradient separations.
- `pylss-makechrom`: Build and plot a chromatogram from retention times.

**Example:**
```bash
# Navigate to the examples directory
cd examples
# Calculate LSS parameters
pylss-lssgen test_caculation_lss_parameter.txt output_test_lss_parameter.txt
```

## Development and Testing

Voluntary contributions are welcome! If you'd like to contribute, please fork the repository, create a feature branch, and submit a Pull Request.

### Running Tests

The project includes a robust test suite using `pytest`. To run the tests, install the optional test dependencies:

```bash
# Install with testing dependencies
pip install ".[test]"

# Run the test suite
pytest tests/
```

### Contribution Guidelines

*   Ensure your code works and passes existing tests.
*   Use `pylint` to check your code (Global Evaluation rate should be >= 9.0).
*   Document your code thoroughly (Parameters, Attributes, Returns, Notes, and References).
*   Provide an example for new features.

## References

[1] *Prediction of retention time in reversed-phase liquid chromatography as a tool for steroid identification*
G.M. Randazzo, D. Tonoli, S. Hambye, D. Guillarme, F. Jeanneret, A. Nurisso, L. Goracci, J. Boccard, Prof. S. Rudaz
Analytica Chimica Acta 2016
doi:10.1016/j.aca.2016.02.014

[2] *High-Performance Gradient Elution: The Practical Application of the Linear-Solvent-Strength Model*
Lloyd R. Snyder, John W. Dolan
ISBN: 978-0-471-70646-5
496 pages
January 2007

## License

PyLSS is distributed under the **GNU Affero General Public License (AGPLv3)**.

- You can use this library where you want, doing what you want.
- You can modify this library and commit changes.
- **If you use this library in a network service, you must make the source code available to your users.**

To know more in detail how the license works, please read the `LICENSE` file or visit https://www.gnu.org/licenses/agpl-3.0.html.

PyLSS is currently the property of Giuseppe Marco Randazzo, who is also the current package maintainer.
