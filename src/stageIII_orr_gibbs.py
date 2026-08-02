#!/usr/bin/env python3
"""Stage III ORR thermodynamics from one fixed VASP/VaspGibbs/VASPsol layout.

The module is intentionally compact and branch-independent. It reads one
public folder convention, calculates CHE adsorption free energies, identifies
the potential-determining step (PDS), compares ORR overpotentials with Pt(111),
and generates static publication figures.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ADSORBATES = ("O", "OH", "OOH")
SURFACE_STATES = ("bare", "O", "OH", "OOH")
EQUILIBRIUM_POTENTIAL_V = 1.23
TOTAL_ORR_FREE_ENERGY_EV = 4.92
PDS_LABELS = {
    "U1": "O2→OOH*",
    "U2": "OOH*→O*",
    "U3": "O*→OH*",
    "U4": "OH*→H2O",
}
FLOAT = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?)"
ELEMENT_COLORS = {"Ni": "#8C8C8C", "Sb": "#D28E2D", "O": "#D62728", "H": "#F7F7F7"}
ELEMENT_SIZES = {"Ni": 48, "Sb": 62, "O": 70, "H": 38}


@dataclass(frozen=True)
class StateEnergy:
    species: str
    state_type: str
    vacuum_energy_eV: float
    gibbs_correction_eV: float
    vacuum_gibbs_eV: float
    solvent_energy_eV: float
    electronic_solvation_shift_eV: float
    vacuum_outcar: str
    frequency_output: str
    solvent_outcar: str


@dataclass(frozen=True)
class Structure:
    comment: str
    lattice: np.ndarray
    symbols: tuple[str, ...]
    positions: np.ndarray


def _as_float(text: str) -> float:
    return float(text.replace("D", "E").replace("d", "e"))


def read_sigma0(outcar: Path) -> float:
    """Read the final VASP energy extrapolated to sigma -> 0."""
    if not outcar.is_file():
        raise FileNotFoundError(f"Required OUTCAR is missing: {outcar}")
    last: float | None = None
    with outcar.open(errors="ignore") as handle:
        for line in handle:
            match = re.search(r"energy\(sigma->0\)\s*=\s*" + FLOAT, line)
            if match:
                last = _as_float(match.group(1))
    if last is None:
        raise ValueError(f"No energy(sigma->0) value found in {outcar}")
    return last


def read_vaspgibbs_correction(markdown: Path) -> float:
    """Read the final ``G - E_dft`` value from VaspGibbs.md."""
    if not markdown.is_file():
        raise FileNotFoundError(f"Required VaspGibbs output is missing: {markdown}")
    text = markdown.read_text(errors="ignore")
    matches = re.findall(r"G\s*-\s*E[_\s-]*dft[^\n\r]*?" + FLOAT, text, flags=re.IGNORECASE)
    if not matches:
        raise ValueError(f"No 'G - E_dft' value found in {markdown}")
    return _as_float(matches[-1])


def read_poscar(path: Path) -> Structure:
    """Read a VASP 5 POSCAR/CONTCAR without requiring ASE or pymatgen."""
    lines = [line.rstrip() for line in path.read_text(errors="ignore").splitlines() if line.strip()]
    if len(lines) < 8:
        raise ValueError(f"Incomplete POSCAR/CONTCAR: {path}")
    scale = float(lines[1].split()[0])
    lattice = np.array([[float(x) for x in lines[i].split()[:3]] for i in range(2, 5)], dtype=float) * scale
    elements = lines[5].split()
    counts = [int(x) for x in lines[6].split()]
    cursor = 7
    if lines[cursor].lower().startswith("s"):
        cursor += 1
    direct = lines[cursor].lower().startswith("d")
    cursor += 1
    n_atoms = sum(counts)
    coords = np.array([[float(x) for x in lines[cursor + i].split()[:3]] for i in range(n_atoms)], dtype=float)
    positions = coords @ lattice if direct else coords * scale
    symbols: list[str] = []
    for element, count in zip(elements, counts):
        symbols.extend([element] * count)
    return Structure(lines[0].strip(), lattice, tuple(symbols), positions)


def validate_layout(data_root: Path) -> list[Path]:
    """Validate the single public folder convention."""
    data_root = data_root.resolve()
    missing: list[Path] = []
    for molecule in ("H2", "H2O"):
        missing.extend(path for path in (
            data_root / "Molecules" / molecule / "Freq" / "OUTCAR",
            data_root / "Molecules" / molecule / "Freq" / "VaspGibbs.md",
            data_root / "Molecules" / molecule / "Sol" / "OUTCAR",
        ) if not path.is_file())
    surfaces = sorted(path for path in data_root.glob("mp-*_*" ) if path.is_dir())
    if not surfaces:
        raise FileNotFoundError(f"No mp-xxxx_hkl folder found in {data_root}")
    for surface in surfaces:
        for state in SURFACE_STATES:
            missing.extend(path for path in (
                surface / state / "CONTCAR",
                surface / state / "OUTCAR",
                surface / state / "Freq" / "VaspGibbs.md",
                surface / state / "Sol" / "OUTCAR",
            ) if not path.is_file())
    if missing:
        raise FileNotFoundError("Incomplete Stage III layout:\n" + "\n".join(f"  - {p}" for p in missing))
    return surfaces


def read_molecule(data_root: Path, molecule: str) -> StateEnergy:
    folder = data_root / "Molecules" / molecule
    e_vac = read_sigma0(folder / "Freq" / "OUTCAR")
    correction = read_vaspgibbs_correction(folder / "Freq" / "VaspGibbs.md")
    e_sol = read_sigma0(folder / "Sol" / "OUTCAR")
    return StateEnergy(
        species=molecule,
        state_type="gas_reference",
        vacuum_energy_eV=e_vac,
        gibbs_correction_eV=correction,
        vacuum_gibbs_eV=e_vac + correction,
        solvent_energy_eV=e_sol,
        electronic_solvation_shift_eV=e_sol - e_vac,
        vacuum_outcar=str(folder / "Freq" / "OUTCAR"),
        frequency_output=str(folder / "Freq" / "VaspGibbs.md"),
        solvent_outcar=str(folder / "Sol" / "OUTCAR"),
    )


def read_surface_state(surface: Path, state: str) -> StateEnergy:
    folder = surface / state
    e_vac = read_sigma0(folder / "OUTCAR")
    correction = read_vaspgibbs_correction(folder / "Freq" / "VaspGibbs.md")
    e_sol = read_sigma0(folder / "Sol" / "OUTCAR")
    return StateEnergy(
        species=state,
        state_type="surface_state",
        vacuum_energy_eV=e_vac,
        gibbs_correction_eV=correction,
        vacuum_gibbs_eV=e_vac + correction,
        solvent_energy_eV=e_sol,
        electronic_solvation_shift_eV=e_sol - e_vac,
        vacuum_outcar=str(folder / "OUTCAR"),
        frequency_output=str(folder / "Freq" / "VaspGibbs.md"),
        solvent_outcar=str(folder / "Sol" / "OUTCAR"),
    )


def molecule_references(h2: StateEnergy, h2o: StateEnergy) -> pd.DataFrame:
    definitions = {"O": (1.0, -1.0), "OH": (1.0, -0.5), "OOH": (2.0, -1.5)}
    labels = {"O": "G(H2O)-G(H2)", "OH": "G(H2O)-0.5G(H2)", "OOH": "2G(H2O)-1.5G(H2)"}
    rows = []
    for adsorbate, (n_h2o, n_h2) in definitions.items():
        electronic = n_h2o * h2o.vacuum_energy_eV + n_h2 * h2.vacuum_energy_eV
        correction = n_h2o * h2o.gibbs_correction_eV + n_h2 * h2.gibbs_correction_eV
        rows.append({
            "adsorbate": adsorbate,
            "reference_definition": labels[adsorbate],
            "electronic_reference_eV": electronic,
            "reference_gibbs_correction_eV": correction,
            "gibbs_reference_eV": electronic + correction,
        })
    return pd.DataFrame(rows)


def adsorption_free_energies(surface: Path, states: dict[str, StateEnergy], references: pd.DataFrame) -> pd.DataFrame:
    ref = references.set_index("adsorbate")
    bare = states["bare"]
    rows = []
    for adsorbate in ADSORBATES:
        ads = states[adsorbate]
        delta_e = ads.vacuum_energy_eV - bare.vacuum_energy_eV - float(ref.loc[adsorbate, "electronic_reference_eV"])
        delta_g_vib = ads.gibbs_correction_eV - bare.gibbs_correction_eV - float(ref.loc[adsorbate, "reference_gibbs_correction_eV"])
        delta_g_vac = delta_e + delta_g_vib
        delta_g_solv = ads.electronic_solvation_shift_eV - bare.electronic_solvation_shift_eV
        delta_g_sol = delta_g_vac + delta_g_solv
        direct = (ads.solvent_energy_eV + ads.gibbs_correction_eV) - (bare.solvent_energy_eV + bare.gibbs_correction_eV) - float(ref.loc[adsorbate, "gibbs_reference_eV"])
        rows.append({
            "slab": surface.name,
            "adsorbate": adsorbate,
            "DeltaE_vac_eV": delta_e,
            "DeltaG_vib_eV": delta_g_vib,
            "DeltaG_solv_eV": delta_g_solv,
            "DeltaG_vac_eV": delta_g_vac,
            "DeltaG_sol_eV": delta_g_sol,
            "closure_error_eV": delta_g_sol - direct,
        })
    frame = pd.DataFrame(rows)
    if not frame["closure_error_eV"].abs().lt(1e-8).all():
        raise ArithmeticError("Solvent decomposition closure check failed")
    return frame


def orr_thermodynamics(adsorption: pd.DataFrame, environment: str) -> dict[str, float | str]:
    col = "DeltaG_vac_eV" if environment == "vacuum" else "DeltaG_sol_eV"
    g = adsorption.set_index("adsorbate")[col]
    steps = {
        "U1": TOTAL_ORR_FREE_ENERGY_EV - float(g["OOH"]),
        "U2": float(g["OOH"] - g["O"]),
        "U3": float(g["O"] - g["OH"]),
        "U4": float(g["OH"]),
    }
    pds_key = min(steps, key=steps.get)
    ul = steps[pds_key]
    return {
        "environment": environment,
        "G_O_eV": float(g["O"]),
        "G_OH_eV": float(g["OH"]),
        "G_OOH_eV": float(g["OOH"]),
        "U1_O2_to_OOH_V": steps["U1"],
        "U2_OOH_to_O_V": steps["U2"],
        "U3_O_to_OH_V": steps["U3"],
        "U4_OH_to_H2O_V": steps["U4"],
        "U_L_ORR_V": ul,
        "eta_ORR_V": EQUILIBRIUM_POTENTIAL_V - ul,
        "PDS_key": pds_key,
        "PDS": PDS_LABELS[pds_key],
    }


def _save_figure(fig: plt.Figure, output_base: Path) -> None:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".svg"), bbox_inches="tight")


def plot_intermediate_structures(surface: Path, output_base: Path) -> plt.Figure:
    """Static top/side projections for bare, O*, OH*, and OOH*."""
    fig, axes = plt.subplots(2, 4, figsize=(7.0, 3.65), constrained_layout=True)
    titles = {"bare": "Bare surface", "O": "O*", "OH": "OH*", "OOH": "OOH*"}
    for col, state in enumerate(SURFACE_STATES):
        structure = read_poscar(surface / state / "CONTCAR")
        symbols = np.array(structure.symbols)
        pos = structure.positions
        metal_mask = np.isin(symbols, ["Ni", "Sb"])
        z_metal_max = pos[metal_mask, 2].max()
        keep = (~metal_mask) | (pos[:, 2] >= z_metal_max - 5.2)
        draw_order = np.argsort(pos[:, 2])
        for row, projection in enumerate(("top", "side")):
            ax = axes[row, col]
            if projection == "top":
                corners = np.array([[0, 0, 0], structure.lattice[0], structure.lattice[0] + structure.lattice[1], structure.lattice[1], [0, 0, 0]])
                ax.plot(corners[:, 0], corners[:, 1], color="0.65", lw=0.7, zorder=0)
            for idx in draw_order:
                if not keep[idx]:
                    continue
                symbol = symbols[idx]
                x, y = (pos[idx, 0], pos[idx, 1]) if projection == "top" else (pos[idx, 0], pos[idx, 2])
                ax.scatter(x, y, s=ELEMENT_SIZES.get(symbol, 45), c=ELEMENT_COLORS.get(symbol, "0.5"), edgecolors="black", linewidths=0.35, zorder=3)
            ax.set_aspect("equal", adjustable="datalim")
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            if row == 0:
                ax.set_title(titles[state], fontsize=8.5, pad=3)
            if col == 0:
                ax.set_ylabel("Top view" if row == 0 else "Side view", fontsize=8)
    handles = [plt.Line2D([0], [0], marker="o", linestyle="", markerfacecolor=ELEMENT_COLORS[e], markeredgecolor="black", markeredgewidth=0.35, markersize=5, label=e) for e in ("Ni", "Sb", "O", "H")]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.015), fontsize=7.5)
    _save_figure(fig, output_base)
    return fig


def plot_adsorption_decomposition(adsorption: pd.DataFrame, output_base: Path) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(3.35, 2.75), constrained_layout=True)
    x = np.arange(len(adsorption))
    width = 0.23
    ax.bar(x - width, adsorption["DeltaE_vac_eV"], width, label=r"$\Delta E_{vac}$")
    ax.bar(x, adsorption["DeltaG_vib_eV"], width, label=r"$\Delta G_{vib}$")
    ax.bar(x + width, adsorption["DeltaG_solv_eV"], width, label=r"$\Delta G_{solv}$")
    ax.axhline(0, color="black", lw=0.7)
    ax.set_xticks(x, [f"{a}*" for a in adsorption["adsorbate"]])
    ax.set_ylabel("Contribution (eV)")
    ax.legend(frameon=False, fontsize=7)
    _save_figure(fig, output_base)
    return fig


def free_energy_levels(row: pd.Series, potential_v: float = EQUILIBRIUM_POTENTIAL_V) -> np.ndarray:
    return np.array([
        TOTAL_ORR_FREE_ENERGY_EV,
        row["G_OOH_eV"] + potential_v,
        row["G_O_eV"] + 2 * potential_v,
        row["G_OH_eV"] + 3 * potential_v,
        4 * potential_v,
    ], dtype=float)


def plot_orr_free_energy(row: pd.Series, output_base: Path, potential_v: float = EQUILIBRIUM_POTENTIAL_V) -> plt.Figure:
    labels = [r"$O_2+*$", r"$OOH^*$", r"$O^*$", r"$OH^*$", r"$2H_2O+*$"]
    levels = free_energy_levels(row, potential_v)
    pds_index = {"U1": 0, "U2": 1, "U3": 2, "U4": 3}[row["PDS_key"]]
    fig, ax = plt.subplots(figsize=(3.35, 2.95), constrained_layout=True)
    for i, energy in enumerate(levels):
        ax.hlines(energy, i - 0.32, i + 0.32, color="black", lw=1.4)
        if i < len(levels) - 1:
            color = "#B2182B" if i == pds_index else "0.45"
            width = 2.0 if i == pds_index else 1.0
            ax.plot([i + 0.32, i + 1 - 0.32], [energy, levels[i + 1]], color=color, lw=width)
    step_dg = levels[pds_index + 1] - levels[pds_index]
    ax.annotate(f"PDS: {row['PDS']}\n$\Delta G_{{PDS}}$ = {step_dg:.3f} eV", xy=(pds_index + 0.5, (levels[pds_index] + levels[pds_index + 1]) / 2), xytext=(0, 18), textcoords="offset points", ha="center", fontsize=7.2, color="#B2182B", arrowprops=dict(arrowstyle="-", color="#B2182B", lw=0.8))
    ax.set_xticks(range(5), labels)
    ax.set_ylabel(r"Free energy at $U=1.23$ V (eV)")
    ax.set_title(f"{row['slab']} — {row['environment']}\n$U_L$={row['U_L_ORR_V']:.3f} V, $\eta_{{ORR}}$={row['eta_ORR_V']:.3f} V", fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    _save_figure(fig, output_base)
    return fig


def plot_pt_comparison(ranking: pd.DataFrame, output_base: Path) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(3.35, 2.8), constrained_layout=True)
    envs = list(ranking["environment"])
    x = np.arange(len(envs))
    width = 0.34
    ax.bar(x - width / 2, ranking["eta_ORR_V"], width, label="mp-10260_111")
    ax.bar(x + width / 2, ranking["Pt111_eta_ORR_V"], width, label="Pt(111)")
    for i, row in ranking.reset_index(drop=True).iterrows():
        ax.text(i - width / 2, row["eta_ORR_V"] + 0.018, row["PDS"], ha="center", va="bottom", fontsize=6.5, rotation=25)
    ax.set_xticks(x, [e.capitalize() for e in envs])
    ax.set_ylabel(r"$\eta_{ORR}$ (V)")
    ax.set_ylim(0, max(ranking["Pt111_eta_ORR_V"].max(), ranking["eta_ORR_V"].max()) + 0.18)
    ax.legend(frameon=False, fontsize=7)
    ax.spines[["top", "right"]].set_visible(False)
    _save_figure(fig, output_base)
    return fig


def run_workflow(data_root: Path, output_dir: Path, pt_reference: Path | None = None) -> dict[str, pd.DataFrame]:
    surfaces = validate_layout(data_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    pt_reference = pt_reference or data_root / "pt111_reference.csv"
    pt = pd.read_csv(pt_reference)
    state_frames = []
    adsorption_frames = []
    orr_rows = []
    h2 = read_molecule(data_root, "H2")
    h2o = read_molecule(data_root, "H2O")
    refs = molecule_references(h2, h2o)
    for surface in surfaces:
        states = {state: read_surface_state(surface, state) for state in SURFACE_STATES}
        sf = pd.DataFrame([asdict(h2), asdict(h2o)] + [asdict(states[s]) for s in SURFACE_STATES])
        sf.insert(0, "slab", surface.name)
        state_frames.append(sf)
        ads = adsorption_free_energies(surface, states, refs)
        adsorption_frames.append(ads)
        for env in ("vacuum", "solvent"):
            orr_rows.append({"slab": surface.name, **orr_thermodynamics(ads, env)})
        plt.close(plot_intermediate_structures(surface, figure_dir / f"Figure_stageIII_intermediates_{surface.name}"))
        plt.close(plot_adsorption_decomposition(ads, figure_dir / f"Figure_stageIII_decomposition_{surface.name}"))
    state = pd.concat(state_frames, ignore_index=True)
    adsorption = pd.concat(adsorption_frames, ignore_index=True)
    orr = pd.DataFrame(orr_rows)
    ranking = orr.merge(pt[["environment", "eta_ORR_V", "PDS"]].rename(columns={"eta_ORR_V": "Pt111_eta_ORR_V", "PDS": "Pt111_PDS"}), on="environment", how="left")
    ranking["delta_eta_vs_Pt111_V"] = ranking["eta_ORR_V"] - ranking["Pt111_eta_ORR_V"]
    ranking["better_than_Pt111"] = ranking["eta_ORR_V"] < ranking["Pt111_eta_ORR_V"]
    ranking["environment"] = pd.Categorical(ranking["environment"], categories=["vacuum", "solvent"], ordered=True)
    ranking = ranking.sort_values(["environment", "eta_ORR_V"]).reset_index(drop=True)
    ranking["environment"] = ranking["environment"].astype(str)
    for _, row in orr.iterrows():
        plt.close(plot_orr_free_energy(row, figure_dir / f"Figure_stageIII_ORR_{row['environment']}_{row['slab']}"))
    plt.close(plot_pt_comparison(ranking, figure_dir / "Figure_stageIII_overpotential_vs_Pt111"))
    tables = {"state_energies": state, "molecular_references": refs, "adsorption_free_energies": adsorption, "orr_results": orr, "pt_ranking": ranking}
    for name, frame in tables.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)
    metadata = {"equilibrium_potential_V": EQUILIBRIUM_POTENTIAL_V, "total_ORR_free_energy_eV": TOTAL_ORR_FREE_ENERGY_EV, "surfaces": [p.name for p in surfaces], "complete_pathway_required": True, "gas_reference_convention": "H2/H2O CHE references retained for vacuum and solvent-aware adsorption free energies"}
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return tables


def verify_demo_results(orr: pd.DataFrame, atol: float = 5e-4) -> None:
    expected = {
        "vacuum": {"eta_ORR_V": 0.4891, "U_L_ORR_V": 0.7409, "PDS": "O*→OH*"},
        "solvent": {"eta_ORR_V": 0.5656, "U_L_ORR_V": 0.6644, "PDS": "OH*→H2O"},
    }
    for env, ref in expected.items():
        row = orr.loc[orr["environment"].eq(env)].iloc[0]
        if abs(float(row["eta_ORR_V"]) - ref["eta_ORR_V"]) > atol or abs(float(row["U_L_ORR_V"]) - ref["U_L_ORR_V"]) > atol or row["PDS"] != ref["PDS"]:
            raise AssertionError(f"Demo verification failed for {env}: {row.to_dict()}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("data/stageIII_demo"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stageIII_demo"))
    parser.add_argument("--pt-reference", type=Path, default=None)
    parser.add_argument("--verify-demo", action="store_true")
    args = parser.parse_args()
    tables = run_workflow(args.data_root, args.output_dir, args.pt_reference)
    if args.verify_demo:
        verify_demo_results(tables["orr_results"])
    print(tables["pt_ranking"][["environment", "slab", "eta_ORR_V", "PDS", "Pt111_eta_ORR_V", "delta_eta_vs_Pt111_V", "better_than_Pt111"]].to_string(index=False))


if __name__ == "__main__":
    main()
