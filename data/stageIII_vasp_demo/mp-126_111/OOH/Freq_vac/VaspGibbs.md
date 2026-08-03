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
| DFT Total Energy |   -344.6513       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.5748301   |      N/A       |      N/A       |
|   Electronic   |        2       |        0       |   5.97308e-05  |  -0.01780874   |
|  Vibrational   |  1.641611e+15  |    0.6539679   |   0.005212455  |   -0.9001255   |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -343.4225     eV  |
|      Entropy      |   0.005358359  eV/K |
| Gibbs Free Energy |   -345.0201     eV  |
|     G - E_dft     |   -0.3687967    eV  |
|        TS         |    1.597595     eV  |
