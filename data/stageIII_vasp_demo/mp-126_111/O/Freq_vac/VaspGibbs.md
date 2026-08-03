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
| DFT Total Energy |   -336.2958       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.2125012   |      N/A       |      N/A       |
|   Electronic   |        1       |        0       |        0       |        0       |
|  Vibrational   |  1.961338e+14  |    0.5899623   |   0.004814692  |   -0.8455381   |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -335.4934     eV  |
|      Entropy      |   0.004900865  eV/K |
| Gibbs Free Energy |   -336.9545     eV  |
|     G - E_dft     |   -0.6587295    eV  |
|        TS         |    1.461193     eV  |
