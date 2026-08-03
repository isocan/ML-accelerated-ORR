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
> **Warning**: frequency 32 is imaginary (i*0.787272). Your structure may not be properly relaxed. Ignoring this frequency.

# Output

## System properties
|     Property     |          Value          |
| :--------------: | :---------------------: |
| DFT Total Energy |   -340.3152       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.4678864   |      N/A       |      N/A       |
|   Electronic   |        2       |        0       |   5.97308e-05  |  -0.01780874   |
|  Vibrational   |  2.141871e+14  |    0.6100694   |   0.004889719  |   -0.8478004   |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -339.2372     eV  |
|      Entropy      |   0.005035624  eV/K |
| Gibbs Free Energy |   -340.7386     eV  |
|     G - E_dft     |   -0.4234153    eV  |
|        TS         |    1.501371     eV  |
