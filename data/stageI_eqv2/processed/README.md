# Stage I screening tables (OC20/EquiformerV2)

The six tables are stored together in `orr_eqv2_stageI_tables.zip` to stay within
GitHub file-size limits. Extract them here with `unzip orr_eqv2_stageI_tables.zip`.
Running the screening notebook writes the same files to this folder.

Produced by `notebooks/02_stageI_eqv2_trajectory_screening.ipynb` from
`ORR_EqV2_Relaxation_Trajectories.zip` (Zenodo). Energies in eV, distances in Å,
forces in eV/Å. To open the trajectory of any row, join `trajectory_relative_path`
to the folder that contains the extracted system folders.

| File | Rows | One row per |
|---|---|---|
| `orr_eqv2_all_trajectory_quality_control.csv` | 72,391 | trajectory (validated or rejected) |
| `orr_eqv2_validated_relaxation_trajectories.csv` | 48,667 | validated trajectory |
| `orr_eqv2_unique_adsorption_site_minima.csv` | 22,885 | distinct adsorption-site instance (lowest energy) |
| `orr_eqv2_adsorption_site_family_minima.csv` | 6,131 | site family per system (lowest energy) |
| `orr_eqv2_global_minimum_configuration_per_system.csv` | 1,654 | slab–adsorbate system (lowest energy; evaluated by SP-DFT) |
| `orr_eqv2_quality_control_summary_by_system.csv` | 1,668 | slab–adsorbate system (counts by outcome) |

## Main columns

| Column | Meaning |
|---|---|
| `system_id` | `<material_id>_<facet>_<adsorbate>`, e.g. `mp-1418_100_OH` |
| `material_id`, `facet`, `surface_id` | Materials Project bulk ID, Miller index, `<material_id>_<facet>` |
| `adsorbate` | `O`, `OH`, or `OOH` |
| `trajectory_label`, `configuration_index`, `trajectory_order` | File stem, integer in the stem, natural-sort position in the folder |
| `trajectory_relative_path` | Trajectory file relative to the data folder |
| `validation_status`, `rejection_reason` | `validated` or `rejected`, and why (quality-control table only) |
| `anomaly_detected`, `anomaly_adsorbate_dissociated`, `anomaly_adsorbate_desorbed`, `anomaly_surface_changed`, `anomaly_adsorbate_intercalated` | FairChem `DetectTrajAnomaly` results (quality-control table only) |
| `n_frames`, `initial_n_atoms`, `final_n_atoms`, `initial_formula`, `final_formula` | Trajectory length and endpoint composition |
| `predicted_adsorption_energy_eV` | OC20/EqV2 adsorption energy stored in the final frame |
| `final_max_force_eV_per_A` | Maximum force on unconstrained atoms in the final frame (threshold 0.05) |
| `relative_energy_within_system_eV`, `energy_rank_within_system` | Energy above, and rank relative to, the lowest validated configuration of the system |
| `n_validated_trajectories_in_system` | Validated trajectories of the system |
| `site_type` | `top`, `bridge`, `3-fold`, `4-fold`, `offcenter_2coord`, or `irregular_<n>coord` |
| `neighbor_string` | Coordinating slab elements, e.g. `Ni-Pt` |
| `site_family` | `<site_type>__<neighbor_string>` (plus contacts of the second OOH oxygen when present) |
| `coordination`, `binding_oxygen_index` | Number of first-shell contacts, and index of the binding O atom |
| `neighbor_indices`, `neighbor_images`, `neighbor_distances_A` | Coordinating atom indices, periodic images, and O–metal distances |
| `site_confidence`, `site_reason`, `site_stable_to_cutoff` | `clear` or `review`, the reason for review, and whether contacts are stable to ±0.04 in the cutoff ratio |
| `binding_mode` | `single_oxygen`, `multi_oxygen` (OOH bound through both O), `distal_only`, or `unbound` |
| `site_instance_key`, `unique_site_key`, `local_site_descriptor` | Keys that identify a site instance within a system and across the dataset |
| `oxygen_contacts_json`, `projection_residual_A` | All selected O–slab contacts, and the in-plane offset used to classify bridges |
| `site_reference_source`, `site_detector_version` | Slab used as periodic-image reference, and detector version |

