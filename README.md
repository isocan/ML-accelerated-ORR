# Multi-Fidelity Machine-Learning Screening of Bimetallic Oxygen Reduction Catalysts across MLIP–DFT Workflows

Code and data accompanying the article of the same title. The repository
reproduces a three-stage workflow for oxygen reduction reaction (ORR) catalyst
screening on bimetallic surfaces. It combines machine-learned interatomic
potentials (MLIPs), adsorption-site analysis, density functional theory (DFT),
vibrational corrections, and implicit solvation.

All analyses are provided as Jupyter notebooks. Each notebook can be opened in
Google Colab from the badge at its top or run locally. Saved outputs are kept in
the notebooks so that the results can be inspected on GitHub without running them.

## Workflow

```text
Open Catalyst bulks (11,410)  →  185 bimetallic bulks from 14 elements
        │                        555 low-index slabs (100, 110, 111) + Pt(111)
        ▼
Stage I    OC20/EquiformerV2 AdsorbML relaxations of O*, OH*, OOH*
           72,391 trajectories → 1,654 validated global minima
           single-point DFT validation → 517 surfaces with complete CHE sets
        │
        ▼
Stage II   Independent re-relaxation of the 24 shortlisted surfaces with
           OC25/eSEN (dispersion, dipole) and AQCat25-EV2 (spin polarization)
        │
        ▼
Stage III  Branch-matched DFT relaxations + VaspGibbs vibrational corrections
           + VASPsol implicit solvation → limiting potential, potential-
           determining step, and overpotential relative to Pt(111)
```

## Notebooks

| # | Notebook | Stage | What it does | Runtime | Input |
|---|---|---|---|---|---|
| 00 | [`00_build_candidate_database`](notebooks/00_build_candidate_database.ipynb) | Database | Builds the frozen 185-bulk inventory from the Open Catalyst bulk database and the Materials Project | CPU | Materials Project API key |
| 01 | [`01_stageI_eqv2_adsorbml_relaxation_demo`](notebooks/01_stageI_eqv2_adsorbml_relaxation_demo.ipynb) | I | Worked example on one surface (Ni₃Sb(111), `mp-10260_111`): AdsorbML placements, EquiformerV2 relaxation, trajectory validation, site analysis, and VASP single-point inputs | GPU | Downloaded automatically |
| 02 | [`02_stageI_eqv2_trajectory_screening`](notebooks/02_stageI_eqv2_trajectory_screening.ipynb) | I | Screens all 72,391 EquiformerV2 trajectories of the study: quality control, FairChem anomaly detection, adsorption-site assignment, and minimum-energy selection | CPU | `ORR_EqV2_Relaxation_Trajectories.zip` (Zenodo) |
| 03 | [`03_stageI_eqv2_adsorption_site_analysis`](notebooks/03_stageI_eqv2_adsorption_site_analysis.ipynb) | I | Adsorption-energy distributions (**Figure S1**), adsorption-site preferences of O\*, OH\*, and OOH\* (**Figure S2**), and descriptive statistics of the site families | CPU | Tables in `data/stageI_eqv2/processed/` |
| 04 | [`04_stageII_esen_oc25_adsorbml_relaxation_CHE`](notebooks/04_stageII_esen_oc25_adsorbml_relaxation_CHE.ipynb) | II | eSEN/OC25 branch on one shortlisted surface: relaxations, CHE adsorption energies, site analysis, and DFT inputs | GPU | Hugging Face token (gated model) |
| 05 | [`05_stageII_aqcat25_adsorbml_relaxation_CHE`](notebooks/05_stageII_aqcat25_adsorbml_relaxation_CHE.ipynb) | II | AQCat25-EV2 spin-aware branch on the same surface | GPU | Hugging Face token (gated model) |
| 06 | [`06_stageIII_vasp_orr_thermodynamics`](notebooks/06_stageIII_vasp_orr_thermodynamics.ipynb) | III | Adsorption free energies, limiting potentials, and overpotentials from VASP outputs for Ni₃Sb(111), CuPt₇(111), and Pt(111) | CPU | `data/demo_data/` |

Notebooks 01, 04, and 05 run the complete procedure on one representative surface
so that it can be executed in a free Colab session. The study applied the same
procedure to all surfaces; the resulting trajectories and DFT calculations are in
the Zenodo dataset.

## Data availability

### Zenodo dataset

The raw data are deposited on Zenodo: **[10.5281/zenodo.24310973](https://doi.org/10.5281/zenodo.24310973)**
(CC BY 4.0). Every DFT archive contains a `README.txt` that describes its layout.

| Archive | Size | Content |
|---|---|---|
| `ORR_EqV2_Relaxation_Trajectories.zip` | 4.3 GB | Stage I OC20/EquiformerV2 relaxation trajectories (ASE `.traj`) for 1,668 slab–adsorbate systems |
| `ORR_DFT_Single_Point.zip` | 121 MB | Stage I single-point DFT on the EquiformerV2 global minima, gas-phase references, and Pt(111); CHE adsorption energies; the 38 slabs excluded from the CHE analysis with their exclusion reasons |
| `ORR_OC25_eSEN_Relaxation_Trajectories.zip` | 219 MB | Stage II OC25/eSEN relaxation trajectories of the shortlisted surfaces |
| `ORR_AQCat25_EV2_Relaxation_Trajectories.zip` | 252 MB | Stage II AQCat25-EV2 relaxation trajectories of the shortlisted surfaces |
| `OC20_EqV2_ORR_DFT_Full_Relax.zip` | 462 MB | Stage III DFT relaxations started from the OC20/EquiformerV2 configurations, with VASPsol and vibrational calculations |
| `OC25_eSEN_ORR_DFT_Full_Relax.zip` | 460 MB | Stage III DFT relaxations started from the OC25/eSEN configurations, with VASPsol and vibrational calculations |
| `AQCat25_EV2_ORR_DFT_Full_Relax.zip` | 495 MB | Stage III spin-polarized DFT relaxations started from the AQCat25-EV2 configurations, with VASPsol and vibrational calculations |

The DFT archives contain `POSCAR`, `INCAR`, `KPOINTS`, `OUTCAR` and/or `OSZICAR`,
and, for vibrational calculations, the VaspGibbs reports. VASP `POTCAR` files are
not distributed because of the VASP license; the potentials used are listed in
each `OUTCAR`.

### Data in this repository

| Path | Content |
|---|---|
| `data/stageI_eqv2/processed/` | The six Stage I screening tables written by notebook 02, packed as `orr_eqv2_stageI_tables.zip`, with a column description in `README.md` |
| `data/demo_data/` | VASP outputs for notebook 06: clean and covered slabs of `mp-10260_111`, `mp-12608_111`, and `mp-126_111`, and the H₂ and H₂O references |

### Where to find the results of the article

| Article item | Source |
|---|---|
| 185-bulk inventory and surface library | Notebook 00 |
| Stage I trajectory screening and the SI table of anomalous systems | Notebook 02 and `data/stageI_eqv2/processed/` |
| Figure S1, Stage I adsorption-energy distributions | Notebook 03 |
| Stage I ML–DFT parity and the excluded-slab table | `ORR_DFT_Single_Point.zip` (`adsorption_energies.csv`, `excluded_slabs/`) |
| Stage II eSEN/OC25 and AQCat25-EV2 screening | Notebooks 04 and 05; trajectories on Zenodo |
| Stage III free energies and overpotentials | Notebook 06; complete calculations in the three `*_DFT_Full_Relax.zip` archives |

## Running the notebooks

### Google Colab

Click the **Open in Colab** badge at the top of a notebook and choose
**Runtime → Run all**.

- Notebooks 01, 04, and 05 need a **T4 GPU** runtime. Each one installs its own
  FairChem environment and restarts the kernel once, as described in its first
  section.
- Notebook 00 needs a Materials Project API key, stored as the Colab secret
  `MP_API_KEY`.
- Notebooks 04 and 05 download gated checkpoints. Request access on Hugging Face
  ([OC25](https://huggingface.co/facebook/OC25),
  [AQCat25-EV2](https://huggingface.co/SandboxAQ/aqcat25-ev2)) and store a read
  token as the Colab secret `HF_TOKEN`.
- Notebooks 02, 03, and 06 run on a CPU.

### Local execution

```bash
git clone https://github.com/isocan/ML-accelerated-ORR.git
cd ML-accelerated-ORR
python -m pip install jupyterlab
jupyter lab
```

Each notebook lists its own dependencies with tested versions in its setup
section. Install them in a separate environment per stage, because the Stage I and
Stage II models require different FairChem versions.

To rerun notebook 02, download `ORR_EqV2_Relaxation_Trajectories.zip` from Zenodo
and extract it into `data/stageI_eqv2/trajectories/`:

```bash
mkdir -p data/stageI_eqv2/trajectories
unzip ORR_EqV2_Relaxation_Trajectories.zip -d data/stageI_eqv2/trajectories
```

## Repository structure

```text
ML-accelerated-ORR/
├── notebooks/
│   ├── 00_build_candidate_database.ipynb
│   ├── 01_stageI_eqv2_adsorbml_relaxation_demo.ipynb
│   ├── 02_stageI_eqv2_trajectory_screening.ipynb
│   ├── 03_stageI_eqv2_adsorption_site_analysis.ipynb
│   ├── 04_stageII_esen_oc25_adsorbml_relaxation_CHE.ipynb
│   ├── 05_stageII_aqcat25_adsorbml_relaxation_CHE.ipynb
│   └── 06_stageIII_vasp_orr_thermodynamics.ipynb
├── data/
│   ├── stageI_eqv2/processed/     Stage I screening tables (notebook 02 output)
│   └── demo_data/                 VASP outputs for notebook 06
├── LICENSE
└── README.md
```

Notebook outputs that are regenerated on each run, such as `figures/` and
`data/stageI_eqv2/trajectories/`, are listed in `.gitignore`.

## Licenses

- Code in this repository: MIT License (see `LICENSE`).
- Data on Zenodo: Creative Commons Attribution 4.0 International.
- Model checkpoints are not redistributed and remain under their own licenses.
  AQCat25-EV2 is licensed for non-commercial use.
- VASP `POTCAR` files are not distributed.

## Citation

If you use this code or data, please cite the article and the dataset:

> Oguz, I. C.; Polese, N.; Mesquita, S.; Thinel, T.; Perrier de la Bathie, H.; Er, S.
> Multi-Fidelity Machine-Learning Screening of Bimetallic Oxygen Reduction
> Catalysts across MLIP–DFT Workflows. *ACS Catalysis* (submitted).

> Oguz, I. C.; Polese, N.; Mesquita, S.; Thinel, T.; Perrier de la Bathie, H.; Er, S.
> Data for "Multi-Fidelity Machine-Learning Screening of Bimetallic Oxygen
> Reduction Catalysts across MLIP–DFT Workflows". Zenodo, 2026.
> https://doi.org/10.5281/zenodo.24310973

Please also cite the methods and data this work builds on:

- OC20 dataset: Chanussot, L. *et al.* *ACS Catal.* **2021**, *11*, 6059–6072.
  [10.1021/acscatal.0c04525](https://doi.org/10.1021/acscatal.0c04525)
- AdsorbML: Lan, J. *et al.* *npj Comput. Mater.* **2023**, *9*, 172.
- EquiformerV2: Liao, Y.-L.; Wood, B. M.; Das, A.; Smidt, T. *ICLR* **2024**.
- OC25: Sahoo, S. J. *et al.* arXiv:2509.17862 (2025).
- eSEN: Fu, X. *et al.* *Proc. Mach. Learn. Res.* **2025**, *267*, 17875–17893.
- AQCat25: Allam, O. *et al.* *npj Comput. Mater.* **2026**, *12*, 226.
  [10.1038/s41524-026-02099-6](https://doi.org/10.1038/s41524-026-02099-6)
- Materials Project: Jain, A. *et al.* *APL Mater.* **2013**, *1*, 011002.
  [10.1063/1.4812323](https://doi.org/10.1063/1.4812323)
- Computational hydrogen electrode: Nørskov, J. K. *et al.* *J. Phys. Chem. B*
  **2004**, *108*, 17886–17892. [10.1021/jp047349j](https://doi.org/10.1021/jp047349j)
- VASPsol: Mathew, K. *et al.* *J. Chem. Phys.* **2014**, *140*, 084106.
  [10.1063/1.4865107](https://doi.org/10.1063/1.4865107)
- VaspGibbs: [github.com/ftherrien/VaspGibbs](https://github.com/ftherrien/VaspGibbs)

## Contact

For questions about the code and data, please contact Ismail Can Oguz
(i.c.oguz@differ.nl), DIFFER – Dutch Institute for Fundamental Energy Research,
Eindhoven, The Netherlands, or open an issue in this repository.
