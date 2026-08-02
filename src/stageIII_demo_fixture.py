"""Materialize the compact mp-10260_111 Stage III demonstration dataset."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

ENERGIES = {
    "H2": (-6.97845601, -0.04369243, -6.80169596),
    "H2O": (-14.17514086, 0.08407561, -14.48114009),
    "bare": (-239.24837110, -0.33213400, -239.29778389),
    "O": (-244.75137033, -0.32673460, -244.87605294),
    "OH": (-249.20376644, -0.12632880, -249.41919036),
    "OOH": (-253.19808593, -0.09620561, -253.46065347),
}

PT111 = (
    "environment,slab,eta_ORR_V,PDS,provenance\n"
    "vacuum,mp-126_111,0.8240,O*→OH*,Stage III OC25/eSEN Pt(111) manuscript benchmark\n"
    "solvent,mp-126_111,0.8320,O*→OH*,Stage III OC25/eSEN Pt(111) manuscript benchmark\n"
)

INCAR_VAC = """SYSTEM = mp-10260_111 RPBE-D3 single-point\nGGA = RP\nIVDW = 12\nENCUT = 500\nISPIN = 1\nLDIPOL = .TRUE.\nIDIPOL = 3\n"""
INCAR_FREQ = """SYSTEM = finite-difference frequencies\nGGA = RP\nIVDW = 12\nENCUT = 500\nIBRION = 5\nNFREE = 2\nPOTIM = 0.015\n"""
INCAR_SOL = """SYSTEM = VASPsol implicit water\nGGA = RP\nIVDW = 12\nENCUT = 500\nLSOL = .TRUE.\nEB_K = 78.4\nLDIPOL = .TRUE.\nIDIPOL = 3\n"""
KPOINTS = """Automatic mesh\n0\nGamma\n4 4 1\n0 0 0\n"""


def _outcar_excerpt(energy: float, label: str) -> str:
    return (
        "# Compact Stage III publication-demo OUTCAR excerpt\n"
        f"# State: {label}\n"
        "# Retains the final energy(sigma->0) and completion marker.\n\n"
        f"  energy  without entropy= {energy: .8f}  energy(sigma->0) = {energy: .8f}\n\n"
        "General timing and accounting informations for this job:\n"
    )


def _vaspgibbs(correction: float, label: str) -> str:
    return (
        f"# VaspGibbs compact report: {label}\n\n"
        "| Quantity | Value | Unit |\n"
        "|---|---:|---|\n"
        f"| G - E_dft | {correction:.8f} | eV |\n"
    )


def materialize_stageIII_demo(destination: Path, overwrite: bool = False) -> Path:
    """Create the fixed Molecules/bare/O/OH/OOH/Freq/Sol demonstration tree."""
    destination = Path(destination)
    marker = destination / ".stageIII_demo_ready"
    if marker.exists() and not overwrite:
        return destination
    if overwrite and destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    repo_root = Path(__file__).resolve().parents[1]
    structures = repo_root / "data" / "stageIII_structures"

    manifest = []
    for molecule in ("H2", "H2O"):
        e_vac, correction, e_sol = ENERGIES[molecule]
        folder = destination / "Molecules" / molecule
        (folder / "Freq").mkdir(parents=True, exist_ok=True)
        (folder / "Sol").mkdir(parents=True, exist_ok=True)
        (folder / "Freq" / "OUTCAR").write_text(_outcar_excerpt(e_vac, molecule + " vacuum"), encoding="utf-8")
        (folder / "Freq" / "VaspGibbs.md").write_text(_vaspgibbs(correction, molecule), encoding="utf-8")
        (folder / "Sol" / "OUTCAR").write_text(_outcar_excerpt(e_sol, molecule + " solvent"), encoding="utf-8")

    for state in ("bare", "O", "OH", "OOH"):
        e_vac, correction, e_sol = ENERGIES[state]
        folder = destination / "mp-10260_111" / state
        (folder / "Freq").mkdir(parents=True, exist_ok=True)
        (folder / "Sol").mkdir(parents=True, exist_ok=True)
        shutil.copy2(structures / f"mp-10260_111_{state}.CONTCAR", folder / "CONTCAR")
        (folder / "OUTCAR").write_text(_outcar_excerpt(e_vac, state + " vacuum"), encoding="utf-8")
        (folder / "Freq" / "VaspGibbs.md").write_text(_vaspgibbs(correction, state), encoding="utf-8")
        (folder / "Sol" / "OUTCAR").write_text(_outcar_excerpt(e_sol, state + " solvent"), encoding="utf-8")
        manifest.append({"state": state, "structure": f"data/stageIII_structures/mp-10260_111_{state}.CONTCAR"})

    settings = destination / "calculation_settings"
    settings.mkdir(parents=True, exist_ok=True)
    (settings / "INCAR_vacuum_relax").write_text(INCAR_VAC, encoding="utf-8")
    (settings / "INCAR_frequency").write_text(INCAR_FREQ, encoding="utf-8")
    (settings / "INCAR_implicit_solvent").write_text(INCAR_SOL, encoding="utf-8")
    (settings / "KPOINTS").write_text(KPOINTS, encoding="utf-8")
    (destination / "pt111_reference.csv").write_text(PT111, encoding="utf-8")
    with (destination / "source_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["state", "structure"])
        writer.writeheader()
        writer.writerows(manifest)
    marker.write_text("ready\n", encoding="utf-8")
    return destination
