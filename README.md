# ML-accelerated ORR catalyst discovery

Reproducibility repository for a multi-fidelity workflow that combines machine-learning interatomic potentials, adsorption-site screening, density-functional theory, vibrational corrections, and implicit solvation for oxygen reduction reaction (ORR) catalyst discovery.

The repository accompanies an ACS Catalysis manuscript and is organized as a notebook-first scientific workflow. Each stage can be inspected independently in Google Colab or executed locally.

## Workflow overview

```text
Bulk candidate database
        │
        ▼
Stage I: EqV2/OC20 adsorption-configuration screening
        │
        ▼
Stage II: eSEN/OC25 and AQCat25 adsorption-energy screening
        │
        ▼
Stage III: VASP + VaspGibbs + VASPsol thermodynamics
        │
        ▼
ORR limiting potential, PDS, overpotential, and Pt(111) comparison
```

## Main notebooks

| Stage | Notebook | Purpose |
|---|---|---|
| I | [`01_stageI_eqv2_adsorbml_relaxation_article_repository.ipynb`](notebooks/01_stageI_eqv2_adsorbml_relaxation_article_repository.ipynb) | EqV2/OC20 relaxation of O*, OH*, and OOH* configurations, trajectory validation, adsorption-site analysis, and minimum-energy selection. |
| II | [`02_stageII_esen_oc25_adsorbml_relaxation_CHE.ipynb`](notebooks/02_stageII_esen_oc25_adsorbml_relaxation_CHE.ipynb) | eSEN/OC25 adsorption relaxation and computational-hydrogen-electrode electronic adsorption energies. |
| II | [`03_stageII_AQCat25_adsorbml_relaxation_CHE.ipynb`](notebooks/03_stageII_AQCat25_adsorbml_relaxation_CHE.ipynb) | AQCat25 adsorption relaxation and computational-hydrogen-electrode electronic adsorption energies. |
| III | [`04_stageIII_real_VASP_ORR.ipynb`](notebooks/04_stageIII_real_VASP_ORR.ipynb) | Reads real VASP outputs, applies VaspGibbs and VASPsol corrections, visualizes adsorbate intermediates, and calculates ORR limiting potentials, PDS values, overpotentials, and Pt(111) comparisons. |

## Supporting notebooks

- [`00_build_candidate_database_colab_fixed.ipynb`](00_build_candidate_database_colab_fixed.ipynb) — construction and filtering of the candidate bulk-material database.
- [`ORR_EqV2_All_Trajectory_Screening_and_Site_Analysis.ipynb`](ORR_EqV2_All_Trajectory_Screening_and_Site_Analysis.ipynb) — full EqV2 trajectory-screening and adsorption-site analysis workflow.

## Stage III demonstration data

The real VASP demonstration data are stored in:

```text
data/stageIII_vasp_demo/
├── Molecules/
│   ├── H2/
│   └── H2O/
├── mp-12608_111/
└── mp-126_111/
```

The Stage III notebook uses:

- the last `energy(sigma->0)` value from each required `OUTCAR`;
- the corresponding `G - E_dft` correction from `Freq_vac/VaspGibbs.md`;
- final structures from `CONTCAR` for ASE and py3Dmol visualization;
- `Sol/OUTCAR` values for solvent-aware surface states;
- vacuum H2 and H2O values as the molecular CHE references in both environments.

`mp-12608_111` is the worked candidate and `mp-126_111` is the directly calculated Pt(111) reference.

## Running the notebooks

### Google Colab

Open a notebook on GitHub and select **Open in Colab**, or use the Colab badge included at the top of supported notebooks. The notebook clones this public repository and reads the committed demonstration data directly; access to the author's Google Drive is not required.

### Local execution

```bash
git clone https://github.com/isocan/ML-accelerated-ORR.git
cd ML-accelerated-ORR

python -m pip install -r requirements-stageIII.txt
jupyter notebook
```

Then open the notebook corresponding to the desired workflow stage.

## Repository structure

```text
ML-accelerated-ORR/
├── 00_build_candidate_database_colab_fixed.ipynb
├── ORR_EqV2_All_Trajectory_Screening_and_Site_Analysis.ipynb
├── notebooks/
│   ├── 01_stageI_eqv2_adsorbml_relaxation_article_repository.ipynb
│   ├── 02_stageII_esen_oc25_adsorbml_relaxation_CHE.ipynb
│   ├── 03_stageII_AQCat25_adsorbml_relaxation_CHE.ipynb
│   └── 04_stageIII_real_VASP_ORR.ipynb
├── data/
│   └── stageIII_vasp_demo/
├── requirements-stageIII.txt
└── README.md
```

## Data and licensing notes

- Licensed VASP `POTCAR` files are not distributed.
- Large restart files such as `WAVECAR` and `CHGCAR` are not required for the published post-processing workflow.
- The committed Stage III data are a representative reproducibility example; the full production calculation archive is outside the scope of this GitHub repository.
- Users must ensure that their use of VASP and any associated pseudopotential data complies with the relevant license terms.

## Citation

Citation information will be updated after publication of the associated ACS Catalysis article.
