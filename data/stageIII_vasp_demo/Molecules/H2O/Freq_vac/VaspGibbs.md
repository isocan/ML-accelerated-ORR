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
*This system is a molecule*
|     Property     |          Value          |
| :--------------: | :---------------------: |
| DFT Total Energy |   -14.17521       eV    |
|   Temperature    |     298.15        K     |
|     Pressure     |      101.3       KPa    |
|      Sigma       |        2                |
|   **P. axes**    |                         |
|       I~1        |   6.58095e-05  eV/THz^2 |
|       I~2        |  0.0001223066  eV/THz^2 |
|       I~3        |  0.0001881161  eV/THz^2 |

## Energy corrections
|      Type      |       Z        |     E (eV)     |    S (eV/K)    |     F (eV)     |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|      ZPE       |      N/A       |    0.5648293   |      N/A       |      N/A       |
|   Electronic   |        1       |        0       |        0       |        0       |
|  Vibrational   |    1.000456    |  9.006873e-05  |  3.413407e-07  |  -1.1702e-05   |
|   Rotational   |    44.54371    |   0.03853887   |  0.0004564146  |  -0.09754113   |
| Translational  |     3002173    |   0.03853887   |   0.001414522  |   -0.3832009   |

## Thermodynamic Quantities
|     Quantity      |        Value        |
| :---------------: | :-----------------: |
|     Enthalpy      |   -13.50752     eV  |
|      Entropy      |   0.001957451  eV/K |
| Gibbs Free Energy |   -14.09113     eV  |
|     G - E_dft     |   0.08407561    eV  |
|        TS         |    0.5836141    eV  |
