#ifdef OMC_BASE_FILE
  #define OMC_FILE OMC_BASE_FILE
#else
  #define OMC_FILE "/home/marius/om_wdir/Buildings.Fluid.FMI.ExportContainers.Examples.FMUs.PumpCircuit/Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit.fmutmp/sources/Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_18spd.c"
#endif
/* spatialDistribution */
#include "Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_model.h"
#if defined(__cplusplus)
extern "C" {
#endif

int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_function_storeSpatialDistribution(DATA *data, threadData_t *threadData)
{
  int equationIndexes[2] = {1,-1};
  
  TRACE_POP
  return 0;
}

int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_function_initSpatialDistribution(DATA *data, threadData_t *threadData)
{

  
  TRACE_POP
  return 0;
}

#if defined(__cplusplus)
}
#endif

