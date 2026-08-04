# VaspGibbs BETA

## Parameters:
 *  ncores : 1
 *  command : srun
 *  vasp : vasp_std
 *  top : 9
 *  list_atoms : []
 *  ibrion : 5
 *  T : 298.15
 *  P : 101.3
 *  mol : False
 *  gen_only : True
 *  version : False

*Vibrational frequencies have been calculated, using existing files.*
> **Warning**: frequency 25 is imaginary (i*0.954068). Your structure may not be properly relaxed. Ignoring this frequency.
> **Warning**: frequency 26 is imaginary (i*1.043721). Your structure may not be properly relaxed. Ignoring this frequency.

# Output

## System properties
|     Property     |          Value          |
| :--------------: | :---------------------: |
| DFT Total Energy |   -330.3232       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.1160619   |      N/A       |      N/A       |
|   Electronic   |        1       |        0       |        0       |        0       |
|  Vibrational   |  2.073727e+13  |    0.5336953   |   0.004432352  |   -0.7878104   |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -329.6734     eV  |
|      Entropy      |   0.004518525  eV/K |
| Gibbs Free Energy |   -331.0206     eV  |
|     G - E_dft     |   -0.697441     eV  |
|        TS         |    1.347198     eV  |
