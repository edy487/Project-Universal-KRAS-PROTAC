# Project: The Cancer Shredder (KRAS G12C PROTAC)

## 🧬 Overview
This project presents a computational design for a PROTAC (Proteolysis Targeting Chimera) targeting the **KRAS G12C** oncoprotein, historically considered "undruggable".

Using a custom Python algorithm (`protac_live.py`), we identified a novel exit vector through the Switch-II pocket, enabling the design of a degrader molecule.

## 💻 Methodology: The "Smart Jiggle" Algorithm
We developed a Monte Carlo-based simulation to scan the protein surface for cryptic tunnels.
* **Input:** PDB Structure 6OIM (KRAS G12C).
* **Technique:** Dynamic Spherical Scanning with atomic flexibility simulation.

## 🏆 Key Results
* **Target Coordinates Found:** X: 4.93, Y: -3.75, Z: 10.28
* **Exit Vector Identified:** Tunnel length of **24 Angstroms** (Collision-free).
* **Proposed Design:** Covalent Warhead (Cys12) + 24Å Linker + VHL Ligand.

## 📂 Files in this Repository
* `protac_live.py` - The source code of the scanning algorithm.
* `Evidence_Screenshots` - Terminal outputs verifying the calculation.
