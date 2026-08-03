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
| DFT Total Energy |   -585.4861       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.7079269   |      N/A       |      N/A       |
|   Electronic   |        2       |        0       |   5.97308e-05  |  -0.01780874   |
|  Vibrational   |  1.081506e+24  |     1.06931    |   0.008355349  |   -1.421838    |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -583.7088     eV  |
|      Entropy      |   0.008501253  eV/K |
| Gibbs Free Energy |   -586.2435     eV  |
|     G - E_dft     |   -0.7574119    eV  |
|        TS         |    2.534648     eV  |
