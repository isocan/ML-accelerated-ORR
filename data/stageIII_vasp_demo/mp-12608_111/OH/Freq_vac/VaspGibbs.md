# VaspGibbs BETA

## Parameters:
 *  ncores : 1
 *  command : srun
 *  vasp : vasp_std
 *  top : 0
 *  list_atoms : ['O', 'H']
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
| DFT Total Energy |   -581.1953       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.6003501   |      N/A       |      N/A       |
|   Electronic   |        2       |        0       |   5.97308e-05  |  -0.01780874   |
|  Vibrational   |  1.825476e+24  |    1.054044    |   0.008349259  |   -1.435287    |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -579.5409     eV  |
|      Entropy      |   0.008495163  eV/K |
| Gibbs Free Energy |   -582.0737     eV  |
|     G - E_dft     |   -0.8784385    eV  |
|        TS         |    2.532833     eV  |
