# VaspGibbs BETA

## Parameters:
 *  ncores : 1
 *  command : srun
 *  vasp : vasp_std
 *  top : 0
 *  list_atoms : []
 *  ibrion : 5
 *  T : 298.15
 *  P : 101.3
 *  mol : True
 *  gen_only : True
 *  version : False

*Vibrational frequencies have been calculated, using existing files.*

# Output

## System properties
*This system is a linear molecule*
|     Property     |          Value          |
| :--------------: | :---------------------: |
| DFT Total Energy |   -6.978462       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |
|      Sigma       |        2                |
|   **P. axes**    |                         |
|       I~1        | -4.390057e-22  eV/THz^2 |
|       I~2        |  2.893843e-05  eV/THz^2 |
|       I~3        |  2.893843e-05  eV/THz^2 |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.2687058   |      N/A       |      N/A       |
|   Electronic   |        1       |        0       |        0       |        0       |
|  Vibrational   |        1       |  4.427625e-10  |  1.556029e-12  | -2.116759e-11  |
|   Rotational   |    1.716134    |   0.02569258   |  0.0001327133  |  -0.01387589   |
| Translational  |    111191.6    |   0.03853887   |   0.001130509  |   -0.2985223   |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -6.619832     eV  |
|      Entropy      |   0.001349395  eV/K |
| Gibbs Free Energy |   -7.022154     eV  |
|     G - E_dft     |  -0.04369243    eV  |
|        TS         |    0.4023223    eV  |
