# 🧬 PROTAC-Linker-Pathfinder: Automated Exit Vector Identification

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Validated-brightgreen?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Oncology%20%7C%20Drug%20Discovery-red?style=for-the-badge)

> **An open-source computational tool for identifying viable linker exit vectors in "undruggable" protein targets using Monte Carlo simulations.**

---

## 📄 Abstract

**Background:**
Proteolysis-Targeting Chimeras (PROTACs) represent a transformative therapeutic modality, enabling the degradation of traditionally "undruggable" oncoproteins. A critical determinant of PROTAC efficacy is the linker design; specifically, identifying a viable exit vector from the target protein’s binding pocket that avoids steric clashes. Traditional "trial-and-error" synthesis is resource-intensive. Consequently, there is an unmet need for accessible computational tools that can predict viable linker trajectories prior to chemical synthesis.

**Methods:**
We developed an open-source structural biology tool in Python to automate the identification of linker exit paths. The algorithm employs a stochastic **Monte Carlo simulation** method ("Smart Jiggle") to explore the 3D conformational space surrounding a bound ligand. The software integrates an **automated ligand detection module** that parses PDB files, identifies the drug molecule regardless of chemical nomenclature, and generates random vectors validated against atomic coordinates to ensure a minimum clearance radius.

**Results:**
The algorithm was validated across a diverse panel of oncological targets:
1.  **BRD4 (Control):** Reproduced known exit vectors for the JQ1 ligand.
2.  **KRAS G12C:** Identified a novel, clash-free trajectory of **24Å** through the Switch-II pocket.
3.  **p53 Y220C:** Successfully navigated the restricted surface crevice, identifying a **1.3Å** exit vector.
4.  **Cereblon (E3 Ligase):** Automatically detected the ligand and mapped exit paths for the E3-recruiting end.

**Keywords:** *Bioinformatics, PROTAC, KRAS G12C, Monte Carlo Simulation, Python, Structure-Based Drug Design, Targeted Protein Degradation.*

---

## 🚀 Features

* **⚡ Automated Ligand Detection:** No need to hardcode residue names (e.g., `LIG`, `UNL`, `EFZ`). The engine scans the PDB file and intelligently selects the target molecule.
* **🎲 Monte Carlo "Smart Jiggle":** Uses stochastic sampling to find escape paths that deterministic algorithms might miss.
* **🛡️ Collision Detection:** Mathematically calculates steric clashes with protein atoms (Van der Waals radii simulation).
* **🌍 Universal Compatibility:** Works on enzymes (deep pockets), transcription factors (flat surfaces), and E3 ligases.

---

## 🛠️ Usage

### 1. Prerequisites
The tool runs on standard Python 3.x libraries. No heavy external dependencies (like NumPy or BioPython) are strictly required for the core engine, making it lightweight and portable.

```bash
git clone [https://github.com/edy487/Project-Universal-KRAS-PROTAC.git](https://github.com/edy487/Project-Universal-KRAS-PROTAC.git)
cd Project-Universal-KRAS-PROTAC
