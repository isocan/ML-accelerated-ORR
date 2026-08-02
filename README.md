# ML-accelerated ORR

Reproducibility notebooks for the multi-fidelity discovery and validation of
bimetallic oxygen-reduction-reaction catalysts.

## Workflow notebooks

1. [`01_stageI_eqv2_adsorbml_relaxation_article_repository.ipynb`](notebooks/01_stageI_eqv2_adsorbml_relaxation_article_repository.ipynb) — Stage I EqV2/OC20 adsorption-configuration screening.
2. [`02_stageII_esen_oc25_adsorbml_relaxation_CHE.ipynb`](notebooks/02_stageII_esen_oc25_adsorbml_relaxation_CHE.ipynb) — Stage II eSEN/OC25 relaxation and CHE electronic adsorption energies.
3. [`03_stageII_AQCat25_adsorbml_relaxation_CHE.ipynb`](notebooks/03_stageII_AQCat25_adsorbml_relaxation_CHE.ipynb) — Stage II AQCat25 relaxation and CHE electronic adsorption energies.
4. [`04_stageIII_vasp_gibbs_overpotential_pt_ranking.ipynb`](notebooks/04_stageIII_vasp_gibbs_overpotential_pt_ranking.ipynb) — Stage III VASP/VaspGibbs/VASPsol free energies, PDS, ORR overpotentials, and Pt(111) ranking.

The Stage III notebook includes a compact `mp-10260_111` demonstration and is
continuously re-executed by GitHub Actions. Generated tables and publication
figures are uploaded as workflow artifacts.

## Stage III local execution

```bash
python -m pip install -r requirements-stageIII.txt

python - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, "src")
from stageIII_demo_fixture import materialize_stageIII_demo
materialize_stageIII_demo(Path("data/stageIII_demo"))
PY

python src/stageIII_orr_gibbs.py \
  --data-root data/stageIII_demo \
  --output-dir outputs/stageIII_demo \
  --verify-demo

python -m jupyter nbconvert \
  --to notebook --execute \
  notebooks/04_stageIII_vasp_gibbs_overpotential_pt_ranking.ipynb \
  --output /tmp/04_stageIII_executed.ipynb
```

Licensed VASP `POTCAR` files are not distributed.
