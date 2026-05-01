# PyLSS: Documentation & User Guide

This document provides a comprehensive overview of the Linear Solvent Strength (LSS) theory, the mathematical logic behind PyLSS, and a step-by-step guide for using the software to optimize Liquid Chromatography (LC) separations.

---

## 1. The Linear Solvent Strength (LSS) Theory

Developed by **Lloyd R. Snyder** and **John W. Dolan**, the Linear Solvent Strength (LSS) theory is the foundational model for predicting retention in reversed-phase liquid chromatography (RPLC).

### 1.1 The Core Equation
The LSS model describes the relationship between the solute retention factor ($k$) and the volume fraction of the organic modifier in the mobile phase ($\phi$):

$$\log(k) = \log(k_w) - S\phi$$

Where:
- **$\log(k_w)$:** The intercept, representing the extrapolated retention factor of the solute in pure water ($\phi = 0$). It relates to the lipophilicity of the molecule.
- **$S$:** The slope of the relationship, which depends on the solute and the organic modifier used (e.g., Acetonitrile or Methanol).
- **$\phi$:** The concentration of the organic solvent (expressed as a fraction from 0.0 to 1.0).

### 1.2 Gradient Elution
In gradient elution, $\phi$ changes over time. For a linear gradient starting at $\phi_0$ and ending at $\phi_f$ over a time $t_g$, the retention time ($t_R$) can be predicted using the integrated form of the LSS equation:

$$t_R = \frac{t_0}{b} \log(2.3 k_0 b + 1) + t_0 + t_D$$

Where:
- **$t_0$:** Column dead time.
- **$t_D$:** System dwell time (dwell volume / flow rate).
- **$k_0$:** Retention factor at the start of the gradient ($\phi_0$).
- **$b$:** The gradient steepness parameter, defined as $b = \frac{V_m S \Delta\phi}{t_g F}$, where $V_m$ is the dead volume and $F$ is the flow rate.

---

## 2. How PyLSS Calculates Parameters

To calculate the unique $\log(k_w)$ and $S$ parameters for a specific compound-column-solvent combination, the software requires experimental data from **two different gradient runs** performed on the same column chemistry.

### 2.1 The Two-Gradient Approach
Usually, two linear gradients with different slopes (different $t_g$) are used (e.g., a "fast" 15-minute gradient and a "slow" 60-minute gradient).
1. The user inputs the measured retention times ($t_{R1}$ and $t_{R2}$) for each compound from these two runs.
2. PyLSS uses a **Nelder-Mead Simplex optimization algorithm** to iteratively solve the gradient equation for both runs simultaneously.
3. The algorithm finds the values of $\log(k_w)$ and $S$ that minimize the difference between the predicted and experimental retention times across both gradients.

Once these parameters are found, the behavior of the molecule is "characterized," allowing the software to predict its retention under **any other** isocratic or gradient condition on that column.

---

## 3. User Guide: From Data to Optimization

### Step 1: Create the Input File
PyLSS uses a standardized `.lss` format. Open a text editor and create a file with the following structure:

```yaml
---
t0: 0.969            # Dead time from a marker (e.g., Uracil)
dwell_volume: 0.375  # System dwell volume (mL)
flow_rate: 0.30      # Flow rate used in the experiments (mL/min)
gradients:
  - [14, 5, 95]      # [Time 1, %B Start, %B End]
  - [60, 5, 95]      # [Time 2, %B Start, %B End]
---
# Molecule Name; tR (Grad 1); tR (Grad 2)
Compound_A; 8.53; 22.11
Compound_B; 9.07; 24.54
Compound_C; 10.48; 28.84
```
*Tip: Use semicolons (`;`) as delimiters for the data section.*

### Step 2: Import the File into the GUI
1. Launch the application by typing `pylss-gui` in your terminal.
2. In the **"Data Input"** tab on the left, click the **"Add"** button.
3. Browse and select your `.lss` file. 
4. The software will automatically parse the parameters and show a preview of your data. Click **"OK"**.
5. Your dataset will now appear in the list on the left.

### Step 3: Create the LSS Model
1. Go to the top menu: **Calculation -> Calculate LSS Parameter**.
2. Select your imported dataset from the dropdown and give your model a name (e.g., "Steroids_C18").
3. Click **"OK"**.
4. The software will perform the optimization. Once finished, the **"Gradient Parameters"** tab will become active, and you will see the calculated $\log(k_w)$ and $S$ values in the data table at the bottom.

### Step 4: Visualize and Optimize
Now that you have a model, you can simulate and optimize your separation without running more experiments.

#### **Playing with Parameters**
In the **"Gradient Parameters"** tab, you can change the Flow Rate, Gradient Start/End, and Gradient Time. The chromatogram in the main window will update in **real-time**, showing you how the peaks move and overlap.

#### **Resolution and Selectivity Maps**
To find the absolute best conditions:
1. Go to **Plot -> Resolution Map**.
2. This generates a heatmap showing the **lowest resolution** found between any two peaks across a wide range of Initial %B and Gradient Times.
3. **Red/Yellow areas** represent poor separation, while **Blue/Green areas** represent high-quality separation.
4. Click on a "good" spot on the map to see those conditions applied to your simulation.

#### **Automatic Elution Window Stretching**
If you want the software to do the work for you:
1. Go to **Calculation -> Automatic Elution Window Stretching**.
2. Define your desired elution window (e.g., you want all compounds to elute between 5 and 20 minutes).
3. Click **"Calculate"**. PyLSS will find the gradient slope that best "stretches" your compounds to fill that time window evenly.

---

## 4. Conclusion
By combining the robust LSS theory with modern optimization algorithms, PyLSS allows chromatographers to drastically reduce method development time. Instead of trial-and-error in the lab, you can characterize your compounds once and find the perfect separation window in minutes.
