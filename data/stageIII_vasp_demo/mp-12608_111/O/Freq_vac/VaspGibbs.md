# VaspGibbs BETA

## Parameters:
 *  ncores : 1
 *  command : srun
 *  vasp : vasp_std
 *  top : 0
 *  list_atoms : ['O']
 *  ibrion : 5
 *  T : 298.15
 *  P : 101.3
 *  mol : False
 *  gen_only : True
 *  version : False

*Vibrational frequencies have been calculated, using existing files.*

# Output

## System properties
|     Property     |          Value          |
| :--------------: | :---------------------: |
| DFT Total Energy |   -577.0993       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.3440954   |      N/A       |      N/A       |
|   Electronic   |        1       |        0       |        0       |        0       |
|  Vibrational   |  3.990581e+22  |    1.008038    |   0.007865506  |   -1.337063    |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -575.7472     eV  |
|      Entropy      |   0.007951679  eV/K |
| Gibbs Free Energy |   -578.1179     eV  |
|     G - E_dft     |    -1.01866     eV  |
|        TS         |    2.370793     eV  |
