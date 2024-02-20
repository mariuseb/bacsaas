#ifdef OMC_BASE_FILE
  #define OMC_FILE OMC_BASE_FILE
#else
  #define OMC_FILE "/home/marius/om_wdir/Buildings.Fluid.FMI.ExportContainers.Examples.FMUs.PumpCircuit/Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit.fmutmp/sources/Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_13opt.c"
#endif
/* Optimization */
#include "Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_model.h"
#include "Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_12jac.h"
#if defined(__cplusplus)
extern "C" {
#endif
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_mayer(DATA* data, modelica_real** res,short *i) {
  throwStreamPrint(NULL, "The model was not compiled with -g=Optimica and the corresponding goal function. The optimization solver cannot be used.");
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_lagrange(DATA* data, modelica_real** res, short * i1, short*i2) {
  throwStreamPrint(NULL, "The model was not compiled with -g=Optimica and the corresponding goal function. The optimization solver cannot be used.");
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_pickUpBoundsForInputsInOptimization(DATA* data, modelica_real* min, modelica_real* max, modelica_real*nominal, modelica_boolean *useNominal, char ** name, modelica_real * start, modelica_real * startTimeOpt) {
  throwStreamPrint(NULL, "The model was not compiled with -g=Optimica and the corresponding goal function. The optimization solver cannot be used.");
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_setInputData(DATA *data, const modelica_boolean file) {
  throwStreamPrint(NULL, "The model was not compiled with -g=Optimica and the corresponding goal function. The optimization solver cannot be used.");
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_getTimeGrid(DATA *data, modelica_integer * nsi, modelica_real**t) {
  throwStreamPrint(NULL, "The model was not compiled with -g=Optimica and the corresponding goal function. The optimization solver cannot be used.");
  return 0;
}
#if defined(__cplusplus)
}
#endif