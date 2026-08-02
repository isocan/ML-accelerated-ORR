from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stageIII_demo_fixture import materialize_stageIII_demo
from stageIII_orr_gibbs import read_poscar, run_workflow, verify_demo_results


def test_stageIII_demo(tmp_path):
    data_root = materialize_stageIII_demo(tmp_path / "stageIII_demo")
    tables = run_workflow(data_root, tmp_path / "results")
    verify_demo_results(tables["orr_results"])
    assert set(tables["adsorption_free_energies"]["adsorbate"]) == {"O", "OH", "OOH"}
    assert tables["adsorption_free_energies"]["closure_error_eV"].abs().max() < 1e-8
    structure = read_poscar(data_root / "mp-10260_111" / "OOH" / "CONTCAR")
    assert len(structure.symbols) == 51
    assert structure.symbols.count("O") == 2
    assert structure.symbols.count("H") == 1
