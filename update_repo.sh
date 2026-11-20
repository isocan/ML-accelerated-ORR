#!/bin/bash
# Run from the root of your ML-accelerated-ORR clone, with repo_update.zip next to it:
#   bash update_repo.sh /path/to/repo_update.zip
set -e
ZIP="${1:-repo_update.zip}"
git pull
git rm -q --ignore-unmatch \
  00_build_candidate_database_colab_fixed.ipynb \
  01_EqV2_Trajectory_Screening.ipynb \
  02_EqV2_Adsorption_Site_Analysis.ipynb \
  notebooks/01_stageI_eqv2_adsorbml_relaxation_article_repository.ipynb \
  notebooks/02_stageII_esen_oc25_adsorbml_relaxation_CHE.ipynb \
  notebooks/03_stageII_AQCat25_adsorbml_relaxation_CHE.ipynb \
  notebooks/04_stageIII_VASP_ORR.ipynb
unzip -o -q "$ZIP" -d .
git add -A
git status --short
echo "Check the list above, then run:"
echo "  git commit -m 'Reorganize notebooks and update README for data availability' && git push"
