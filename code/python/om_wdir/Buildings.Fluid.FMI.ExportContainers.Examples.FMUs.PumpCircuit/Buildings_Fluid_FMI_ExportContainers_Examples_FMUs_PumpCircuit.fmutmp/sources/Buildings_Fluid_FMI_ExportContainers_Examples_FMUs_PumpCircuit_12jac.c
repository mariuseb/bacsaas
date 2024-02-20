#ifdef OMC_BASE_FILE
  #define OMC_FILE OMC_BASE_FILE
#else
  #define OMC_FILE "/home/marius/om_wdir/Buildings.Fluid.FMI.ExportContainers.Examples.FMUs.PumpCircuit/Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit.fmutmp/sources/Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_12jac.c"
#endif
/* Jacobians 7 */
#include "Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_model.h"
#include "Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_12jac.h"
#include "simulation/jacobian_util.h"
#include "util/omc_file.h"
/* constant equations */
/* dynamic equations */

/*
equation index: 945
type: SIMPLE_ASSIGN
$cse8.T.$pDERFMIDER.dummyVarFMIDER = Tsup.SeedFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_945(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 0;
  const int equationIndexes[2] = {1,945};
  jacobian->tmpVars[11] /* $cse8.T.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = jacobian->seedVars[3] /* Tsup.SeedFMIDER SEED_VAR */;
  TRACE_POP
}

/*
equation index: 946
type: SIMPLE_ASSIGN
hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER = 4184.0 * $cse8.T.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_946(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 1;
  const int equationIndexes[2] = {1,946};
  jacobian->tmpVars[38] /* hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = (4184.0) * (jacobian->tmpVars[11] /* $cse8.T.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */);
  TRACE_POP
}

/*
equation index: 947
type: SIMPLE_ASSIGN
$DER.fan.filter.s.$pDERFMIDER.dummyVarFMIDER[2] = fan.filter.u_nom * (fan.filter.s.SeedFMIDER[1] - fan.filter.s.SeedFMIDER[2]) * fan.filter.w_u
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_947(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 2;
  const int equationIndexes[2] = {1,947};
#line 52 "/home/marius/modelica-buildings/Buildings/Fluid/BaseClasses/ActuatorFilter.mo"
  jacobian->resultVars[1] /* der(fan.filter.s.$pDERFMIDER.dummyVarFMIDER[2]) JACOBIAN_VAR */ = ((data->simulationInfo->realParameter[195] /* fan.filter.u_nom PARAM */)) * ((jacobian->seedVars[0] /* fan.filter.s.SeedFMIDER[1] SEED_VAR */ - jacobian->seedVars[1] /* fan.filter.s.SeedFMIDER[2] SEED_VAR */) * ((data->simulationInfo->realParameter[197] /* fan.filter.w_u PARAM */)));
#line 57 OMC_FILE
  TRACE_POP
}

/*
equation index: 948
type: SIMPLE_ASSIGN
fluPor.2.m_flow.$pDERFMIDER.dummyVarFMIDER = (-fan.filter.u_nom) * fan.filter.s.SeedFMIDER[2]
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_948(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 3;
  const int equationIndexes[2] = {1,948};
#line 25 "/home/marius/modelica-buildings/Buildings/Fluid/BaseClasses/ActuatorFilter.mo"
  jacobian->resultVars[8] /* fluPor.2.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */ = ((-(data->simulationInfo->realParameter[195] /* fan.filter.u_nom PARAM */))) * (jacobian->seedVars[1] /* fan.filter.s.SeedFMIDER[2] SEED_VAR */);
#line 74 OMC_FILE
  TRACE_POP
}

/*
equation index: 949
type: SIMPLE_ASSIGN
fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER = -fluPor.2.m_flow.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_949(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 4;
  const int equationIndexes[2] = {1,949};
#line 13 "/home/marius/.openmodelica/libraries/Modelica 4.0.0+maint.om/Fluid/Interfaces.mo"
  jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */ = (-jacobian->resultVars[8] /* fluPor.2.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */);
#line 91 OMC_FILE
  TRACE_POP
}

/*
equation index: 950
type: SIMPLE_ASSIGN
fan.vol.steBal.m_flowInv.$pDERFMIDER.dummyVarFMIDER = if noEvent(fluPor[1].m_flow > 0.001 * fan.vol.steBal.m_flow_small) or noEvent(fluPor[1].m_flow < (-0.001) * fan.vol.steBal.m_flow_small) then (-fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER) / fluPor[1].m_flow ^ 2.0 else if noEvent(fluPor[1].m_flow < 0.5 * fan.vol.steBal.deltaReg) and noEvent(fluPor[1].m_flow > (-0.5) * fan.vol.steBal.deltaReg) then fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER * fan.vol.steBal.deltaReg ^ 2.0 / fan.vol.steBal.deltaReg ^ 4.0 else (if noEvent(fluPor[1].m_flow >= 0.0) then 1.0 else -1.0) * sign(fluPor[1].m_flow) * fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER * (abs(fluPor[1].m_flow) * (abs(fluPor[1].m_flow) * (abs(fluPor[1].m_flow) * (abs(fluPor[1].m_flow) * fan.vol.steBal.fReg + fan.vol.steBal.eReg + abs(fluPor[1].m_flow) * fan.vol.steBal.fReg) + fan.vol.steBal.dReg + abs(fluPor[1].m_flow) * (fan.vol.steBal.eReg + abs(fluPor[1].m_flow) * fan.vol.steBal.fReg)) + fan.vol.steBal.cReg + abs(fluPor[1].m_flow) * (fan.vol.steBal.dReg + abs(fluPor[1].m_flow) * (fan.vol.steBal.eReg + abs(fluPor[1].m_flow) * fan.vol.steBal.fReg))) + fan.vol.steBal.bReg + abs(fluPor[1].m_flow) * (fan.vol.steBal.cReg + abs(fluPor[1].m_flow) * (fan.vol.steBal.dReg + abs(fluPor[1].m_flow) * (fan.vol.steBal.eReg + abs(fluPor[1].m_flow) * fan.vol.steBal.fReg))))
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_950(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 5;
  const int equationIndexes[2] = {1,950};
  modelica_boolean tmp0;
  modelica_boolean tmp1;
  modelica_real tmp2;
  modelica_boolean tmp3;
  modelica_boolean tmp4;
  modelica_real tmp5;
  modelica_real tmp6;
  modelica_boolean tmp7;
  modelica_boolean tmp8;
  modelica_real tmp9;
  modelica_boolean tmp10;
  modelica_real tmp11;
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  tmp0 = Greater((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),(0.001) * ((data->simulationInfo->realParameter[294] /* fan.vol.steBal.m_flow_small PARAM */)));
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  tmp1 = Less((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),(-0.001) * ((data->simulationInfo->realParameter[294] /* fan.vol.steBal.m_flow_small PARAM */)));
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  tmp10 = (modelica_boolean)(tmp0 || tmp1);
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  if(tmp10)
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  {
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    tmp2 = (data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */);
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    tmp11 = DIVISION((-jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */),(tmp2 * tmp2),"fluPor[1].m_flow ^ 2.0");
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  }
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  else
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  {
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    tmp3 = Less((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),(0.5) * ((data->simulationInfo->realParameter[290] /* fan.vol.steBal.deltaReg PARAM */)));
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    tmp4 = Greater((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),(-0.5) * ((data->simulationInfo->realParameter[290] /* fan.vol.steBal.deltaReg PARAM */)));
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    tmp8 = (modelica_boolean)(tmp3 && tmp4);
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    if(tmp8)
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    {
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
      tmp5 = (data->simulationInfo->realParameter[290] /* fan.vol.steBal.deltaReg PARAM */);
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
      tmp6 = (data->simulationInfo->realParameter[290] /* fan.vol.steBal.deltaReg PARAM */);
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
      tmp6 *= tmp6;
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
      tmp9 = DIVISION((jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */) * ((tmp5 * tmp5)),(tmp6 * tmp6),"fan.vol.steBal.deltaReg ^ 4.0");
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    }
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    else
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    {
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
      tmp7 = GreaterEq((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),0.0);
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
      tmp9 = ((tmp7?1.0:-1.0)) * (((sign((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * (jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */)) * ((fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[292] /* fan.vol.steBal.fReg PARAM */)) + (data->simulationInfo->realParameter[291] /* fan.vol.steBal.eReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[292] /* fan.vol.steBal.fReg PARAM */))) + (data->simulationInfo->realParameter[288] /* fan.vol.steBal.dReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[291] /* fan.vol.steBal.eReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[292] /* fan.vol.steBal.fReg PARAM */)))) + (data->simulationInfo->realParameter[286] /* fan.vol.steBal.cReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[288] /* fan.vol.steBal.dReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[291] /* fan.vol.steBal.eReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[292] /* fan.vol.steBal.fReg PARAM */))))) + (data->simulationInfo->realParameter[285] /* fan.vol.steBal.bReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[286] /* fan.vol.steBal.cReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[288] /* fan.vol.steBal.dReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[291] /* fan.vol.steBal.eReg PARAM */) + (fabs((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * ((data->simulationInfo->realParameter[292] /* fan.vol.steBal.fReg PARAM */)))))));
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    }
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
    tmp11 = tmp9;
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  }
#line 136 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  jacobian->tmpVars[35] /* fan.vol.steBal.m_flowInv.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = tmp11;
#line 174 OMC_FILE
  TRACE_POP
}

/*
equation index: 951
type: SIMPLE_ASSIGN
fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER = 0.001004433569776996 * fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_951(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 6;
  const int equationIndexes[2] = {1,951};
#line 451 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = (0.001004433569776996) * (jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */);
#line 191 OMC_FILE
  TRACE_POP
}

/*
equation index: 952
type: SIMPLE_ASSIGN
resSup.dp.$pDERFMIDER.dummyVarFMIDER = fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER * resSup.coeff
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_952(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 7;
  const int equationIndexes[2] = {1,952};
#line 38 "/home/marius/modelica-buildings/Buildings/Fluid/FixedResistances/PressureDrop.mo"
  jacobian->tmpVars[49] /* resSup.dp.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = (jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */) * ((data->simulationInfo->realParameter[357] /* resSup.coeff PARAM */));
#line 208 OMC_FILE
  TRACE_POP
}

/*
equation index: 953
type: SIMPLE_ASSIGN
$cse8.p.$pDERFMIDER.dummyVarFMIDER = -(if hea.preDro.dp_nominal_pos > 1e-15 then fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER * $DER$Buildings$PFluid$PBaseClasses$PFlowModels$PbasicFlowFunction_m_flow(fluPor[1].m_flow, hea.preDro.k, hea.preDro.m_flow_turbulent, 1.0, 0.0, 0.0) else 0.0)
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_953(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 8;
  const int equationIndexes[2] = {1,953};
  modelica_boolean tmp12;
  tmp12 = Greater((data->simulationInfo->realParameter[326] /* hea.preDro.dp_nominal_pos PARAM */),1e-15);
  jacobian->tmpVars[12] /* $cse8.p.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = (-((tmp12?(jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */) * (omc__omcQ_24DER_24Buildings_24PFluid_24PBaseClasses_24PFlowModels_24PbasicFlowFunction_5F_5Fm_5F_5Fflow(threadData, (data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */), (data->simulationInfo->realParameter[328] /* hea.preDro.k PARAM */), (data->simulationInfo->realParameter[332] /* hea.preDro.m_flow_turbulent PARAM */), 1.0, 0.0, 0.0)):0.0)));
  TRACE_POP
}

/*
equation index: 954
type: SIMPLE_ASSIGN
fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER = resSup.dp.$pDERFMIDER.dummyVarFMIDER - $cse8.p.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_954(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 9;
  const int equationIndexes[2] = {1,954};
#line 47 "/home/marius/modelica-buildings/Buildings/Fluid/Sensors/RelativePressure.mo"
  jacobian->tmpVars[34] /* fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = jacobian->tmpVars[49] /* resSup.dp.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ - jacobian->tmpVars[12] /* $cse8.p.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */;
#line 242 OMC_FILE
  TRACE_POP
}

/*
equation index: 955
type: SIMPLE_ASSIGN
fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER = smooth(0, if noEvent(fan.senRelPre.p_rel * fan.VMachine_flow > 0.5 * fan.eff.deltaP) then fan.senRelPre.p_rel * fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER + fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER * fan.VMachine_flow else if noEvent(fan.senRelPre.p_rel * fan.VMachine_flow < (-0.5) * fan.eff.deltaP) then 0.0 else if noEvent(0.5 * fan.eff.deltaP > 0.0) then ((-fan.senRelPre.p_rel) * fan.VMachine_flow * 2.0 * ((4.0 * (fan.senRelPre.p_rel * fan.VMachine_flow / fan.eff.deltaP) ^ 2.0 - 3.0) * (fan.senRelPre.p_rel * fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER + fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER * fan.VMachine_flow) + 4.0 * 2.0 * fan.senRelPre.p_rel * fan.VMachine_flow / fan.eff.deltaP * (fan.senRelPre.p_rel * fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER * fan.eff.deltaP / fan.eff.deltaP ^ 2.0 + fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER * fan.VMachine_flow / fan.eff.deltaP) * fan.senRelPre.p_rel * fan.VMachine_flow) + ((-fan.senRelPre.p_rel) * fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER - fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER * fan.VMachine_flow) * (4.0 * (fan.senRelPre.p_rel * fan.VMachine_flow / fan.eff.deltaP) ^ 2.0 - 3.0) * 2.0 * fan.senRelPre.p_rel * fan.VMachine_flow) * fan.eff.deltaP * 4.0 / (fan.eff.deltaP * 4.0) ^ 2.0 + 0.5 * (fan.senRelPre.p_rel * fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER + fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER * fan.VMachine_flow) else 0.5 * (fan.senRelPre.p_rel * fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER + fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER * fan.VMachine_flow))
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_955(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 10;
  const int equationIndexes[2] = {1,955};
  modelica_boolean tmp13;
  modelica_boolean tmp14;
  modelica_boolean tmp15;
  modelica_real tmp16;
  modelica_real tmp17;
  modelica_real tmp18;
  modelica_real tmp19;
  modelica_boolean tmp20;
  modelica_real tmp21;
  modelica_boolean tmp22;
  modelica_real tmp23;
  modelica_boolean tmp24;
  modelica_real tmp25;
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  tmp13 = Greater(((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)),(0.5) * ((data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */)));
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  tmp24 = (modelica_boolean)tmp13;
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  if(tmp24)
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  {
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    tmp25 = ((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * (jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + (jacobian->tmpVars[34] /* fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */));
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  }
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  else
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  {
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    tmp14 = Less(((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)),(-0.5) * ((data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */)));
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    tmp22 = (modelica_boolean)tmp14;
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    if(tmp22)
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    {
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      tmp23 = 0.0;
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    }
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    else
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    {
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      tmp15 = Greater((0.5) * ((data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */)),0.0);
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      tmp20 = (modelica_boolean)tmp15;
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      if(tmp20)
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      {
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
        tmp16 = ((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * (DIVISION((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */),(data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */),"fan.eff.deltaP"));
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
        tmp17 = (data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */);
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
        tmp18 = ((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * (DIVISION((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */),(data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */),"fan.eff.deltaP"));
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
        tmp19 = ((data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */)) * (4.0);
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
        tmp21 = DIVISION(((((-(data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */))) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */))) * ((2.0) * (((4.0) * ((tmp16 * tmp16)) - 3.0) * (((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * (jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + (jacobian->tmpVars[34] /* fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */))) + ((4.0) * (((2.0) * (((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * (DIVISION((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */),(data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */),"fan.eff.deltaP")))) * (((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * (DIVISION((jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */)),(tmp17 * tmp17),"fan.eff.deltaP ^ 2.0")) + (jacobian->tmpVars[34] /* fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * (DIVISION((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */),(data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */),"fan.eff.deltaP"))))) * (((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */))))) + (((-(data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */))) * (jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) - ((jacobian->tmpVars[34] /* fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)))) * (((4.0) * ((tmp18 * tmp18)) - 3.0) * ((2.0) * (((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)))))) * (((data->simulationInfo->realParameter[36] /* fan.eff.deltaP PARAM */)) * (4.0)),(tmp19 * tmp19),"(fan.eff.deltaP * 4.0) ^ 2.0") + (0.5) * (((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * (jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + (jacobian->tmpVars[34] /* fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)));
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      }
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      else
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      {
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
        tmp21 = (0.5) * (((data->localData[0]->realVars[51] /* fan.senRelPre.p_rel variable */)) * (jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + (jacobian->tmpVars[34] /* fan.senRelPre.p_rel.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)));
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      }
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
      tmp23 = tmp21;
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    }
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
    tmp25 = tmp23;
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  }
#line 590 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  jacobian->tmpVars[22] /* fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = tmp25;
#line 340 OMC_FILE
  TRACE_POP
}

/*
equation index: 956
type: SIMPLE_ASSIGN
fan.eff.P_internal.$pDERFMIDER.dummyVarFMIDER = 1.428571428571429 * fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_956(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 11;
  const int equationIndexes[2] = {1,956};
#line 654 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  jacobian->tmpVars[21] /* fan.eff.P_internal.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = (1.428571428571429) * (jacobian->tmpVars[22] /* fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */);
#line 357 OMC_FILE
  TRACE_POP
}

/*
equation index: 957
type: SIMPLE_ASSIGN
fan.P.$pDERFMIDER.dummyVarFMIDER = 2.040816326530613 * fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_957(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 12;
  const int equationIndexes[2] = {1,957};
#line 607 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/FlowMachineInterface.mo"
  jacobian->tmpVars[16] /* fan.P.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = (2.040816326530613) * (jacobian->tmpVars[22] /* fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */);
#line 374 OMC_FILE
  TRACE_POP
}

/*
equation index: 958
type: SIMPLE_ASSIGN
fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER = (if fan.per.motorCooledByFluid then fan.P.$pDERFMIDER.dummyVarFMIDER else fan.eff.P_internal.$pDERFMIDER.dummyVarFMIDER) - fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_958(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 13;
  const int equationIndexes[2] = {1,958};
#line 59 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  jacobian->tmpVars[27] /* fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = ((data->simulationInfo->booleanParameter[26] /* fan.per.motorCooledByFluid PARAM */)?jacobian->tmpVars[16] /* fan.P.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */:jacobian->tmpVars[21] /* fan.eff.P_internal.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) - jacobian->tmpVars[22] /* fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */;
#line 391 OMC_FILE
  TRACE_POP
}

/*
equation index: 959
type: SIMPLE_ASSIGN
fan.PToMed.u1.$pDERFMIDER.dummyVarFMIDER = smooth(0, if noEvent(abs(fan.VMachine_flow) + (-2.0) * fan.heaDis.delta_V_flow > fan.heaDis.delta_V_flow) then fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER else if noEvent(abs(fan.VMachine_flow) + (-2.0) * fan.heaDis.delta_V_flow < (-fan.heaDis.delta_V_flow)) then 0.0 else if noEvent(fan.heaDis.delta_V_flow > 0.0) then 0.25 * ((2.0 - abs(fan.VMachine_flow) / fan.heaDis.delta_V_flow) * ((abs(fan.VMachine_flow) / fan.heaDis.delta_V_flow + -2.0) ^ 2.0 - 3.0) * fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER + ((2.0 - abs(fan.VMachine_flow) / fan.heaDis.delta_V_flow) * 2.0 * (abs(fan.VMachine_flow) / fan.heaDis.delta_V_flow + -2.0) * sign(fan.VMachine_flow) * fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER * fan.heaDis.delta_V_flow / fan.heaDis.delta_V_flow ^ 2.0 - sign(fan.VMachine_flow) * fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER * fan.heaDis.delta_V_flow / fan.heaDis.delta_V_flow ^ 2.0 * ((abs(fan.VMachine_flow) / fan.heaDis.delta_V_flow + -2.0) ^ 2.0 - 3.0)) * fan.heaDis.QThe_flow) + 0.5 * fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER else 0.5 * fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER)
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_959(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 14;
  const int equationIndexes[2] = {1,959};
  modelica_boolean tmp26;
  modelica_boolean tmp27;
  modelica_boolean tmp28;
  modelica_real tmp29;
  modelica_real tmp30;
  modelica_real tmp31;
  modelica_real tmp32;
  modelica_boolean tmp33;
  modelica_real tmp34;
  modelica_boolean tmp35;
  modelica_real tmp36;
  modelica_boolean tmp37;
  modelica_real tmp38;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  tmp26 = Greater(fabs((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)) + (-2.0) * ((data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */)),(data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */));
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  tmp37 = (modelica_boolean)tmp26;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  if(tmp37)
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  {
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    tmp38 = jacobian->tmpVars[27] /* fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  }
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  else
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  {
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    tmp27 = Less(fabs((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)) + (-2.0) * ((data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */)),(-(data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */)));
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    tmp35 = (modelica_boolean)tmp27;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    if(tmp35)
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    {
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      tmp36 = 0.0;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    }
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    else
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    {
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      tmp28 = Greater((data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */),0.0);
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      tmp33 = (modelica_boolean)tmp28;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      if(tmp33)
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      {
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
        tmp29 = DIVISION(fabs((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)),(data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */),"fan.heaDis.delta_V_flow") + -2.0;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
        tmp30 = (data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */);
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
        tmp31 = (data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */);
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
        tmp32 = DIVISION(fabs((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)),(data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */),"fan.heaDis.delta_V_flow") + -2.0;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
        tmp34 = (0.25) * (((2.0 - (DIVISION(fabs((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)),(data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */),"fan.heaDis.delta_V_flow"))) * ((tmp29 * tmp29) - 3.0)) * (jacobian->tmpVars[27] /* fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + ((2.0 - (DIVISION(fabs((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)),(data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */),"fan.heaDis.delta_V_flow"))) * (DIVISION(((2.0) * (DIVISION(fabs((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */)),(data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */),"fan.heaDis.delta_V_flow") + -2.0)) * (((sign((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */))) * (jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */)) * ((data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */))),(tmp30 * tmp30),"fan.heaDis.delta_V_flow ^ 2.0")) - ((DIVISION(((sign((data->localData[0]->realVars[27] /* fan.VMachine_flow variable */))) * (jacobian->tmpVars[18] /* fan.VMachine_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */)) * ((data->simulationInfo->realParameter[202] /* fan.heaDis.delta_V_flow PARAM */)),(tmp31 * tmp31),"fan.heaDis.delta_V_flow ^ 2.0")) * ((tmp32 * tmp32) - 3.0))) * ((data->localData[0]->realVars[40] /* fan.heaDis.QThe_flow variable */))) + (0.5) * (jacobian->tmpVars[27] /* fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */);
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      }
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      else
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      {
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
        tmp34 = (0.5) * (jacobian->tmpVars[27] /* fan.heaDis.QThe_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */);
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      }
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
      tmp36 = tmp34;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    }
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
    tmp38 = tmp36;
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  }
#line 62 "/home/marius/modelica-buildings/Buildings/Fluid/Movers/BaseClasses/PowerInterface.mo"
  jacobian->tmpVars[17] /* fan.PToMed.u1.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = tmp38;
#line 489 OMC_FILE
  TRACE_POP
}

/*
equation index: 960
type: SIMPLE_ASSIGN
fan.prePow.Q_flow.$pDERFMIDER.dummyVarFMIDER = fan.PToMed.u1.$pDERFMIDER.dummyVarFMIDER + fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_960(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 15;
  const int equationIndexes[2] = {1,960};
#line 880 "/home/marius/.openmodelica/libraries/Modelica 4.0.0+maint.om/Blocks/Math.mo"
  jacobian->tmpVars[32] /* fan.prePow.Q_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = jacobian->tmpVars[17] /* fan.PToMed.u1.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ + jacobian->tmpVars[22] /* fan.eff.WFlo.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */;
#line 506 OMC_FILE
  TRACE_POP
}

/*
equation index: 961
type: SIMPLE_ASSIGN
hea.outCon.m_flow_pos.$pDERFMIDER.dummyVarFMIDER = smooth(0, if noEvent(fluPor[1].m_flow > hea.outCon.m_flow_small) then fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER else if noEvent(fluPor[1].m_flow < (-hea.outCon.m_flow_small)) then 0.0 else if noEvent(hea.outCon.m_flow_small > 0.0) then 0.25 * ((3.0 - (fluPor[1].m_flow / hea.outCon.m_flow_small) ^ 2.0) * 2.0 * fluPor[1].m_flow * fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER - 2.0 * fluPor[1].m_flow / hea.outCon.m_flow_small * fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER * hea.outCon.m_flow_small / hea.outCon.m_flow_small ^ 2.0 * fluPor[1].m_flow ^ 2.0) * hea.outCon.m_flow_small / hea.outCon.m_flow_small ^ 2.0 + 0.5 * fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER else 0.5 * fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER)
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_961(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 16;
  const int equationIndexes[2] = {1,961};
  modelica_boolean tmp39;
  modelica_boolean tmp40;
  modelica_boolean tmp41;
  modelica_real tmp42;
  modelica_real tmp43;
  modelica_real tmp44;
  modelica_real tmp45;
  modelica_boolean tmp46;
  modelica_real tmp47;
  modelica_boolean tmp48;
  modelica_real tmp49;
  modelica_boolean tmp50;
  modelica_real tmp51;
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  tmp39 = Greater((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),(data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */));
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  tmp50 = (modelica_boolean)tmp39;
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  if(tmp50)
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  {
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    tmp51 = jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */;
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  }
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  else
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  {
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    tmp40 = Less((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),(-(data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */)));
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    tmp48 = (modelica_boolean)tmp40;
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    if(tmp48)
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    {
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      tmp49 = 0.0;
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    }
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    else
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    {
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      tmp41 = Greater((data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */),0.0);
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      tmp46 = (modelica_boolean)tmp41;
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      if(tmp46)
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      {
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp42 = DIVISION((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),(data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */),"hea.outCon.m_flow_small");
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp43 = (data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */);
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp44 = (data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */);
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp45 = (data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */);
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp47 = (0.25) * (DIVISION(((3.0 - ((tmp42 * tmp42))) * (((2.0) * ((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */))) * (jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */)) - ((DIVISION(((2.0) * (DIVISION((data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */),(data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */),"hea.outCon.m_flow_small"))) * ((jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */) * ((data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */))),(tmp43 * tmp43),"hea.outCon.m_flow_small ^ 2.0")) * ((tmp44 * tmp44)))) * ((data->simulationInfo->realParameter[318] /* hea.outCon.m_flow_small PARAM */)),(tmp45 * tmp45),"hea.outCon.m_flow_small ^ 2.0")) + (0.5) * (jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */);
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      }
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      else
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      {
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp47 = (0.5) * (jacobian->resultVars[7] /* fluPor.1.m_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */);
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      }
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      tmp49 = tmp47;
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    }
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    tmp51 = tmp49;
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  }
#line 205 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  jacobian->tmpVars[42] /* hea.outCon.m_flow_pos.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = tmp51;
#line 604 OMC_FILE
  TRACE_POP
}

/*
equation index: 962
type: SIMPLE_ASSIGN
fan.filter.x.$pDERFMIDER.dummyVarFMIDER[1] = fan.filter.u_nom * fan.filter.s.SeedFMIDER[1]
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_962(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 17;
  const int equationIndexes[2] = {1,962};
#line 25 "/home/marius/modelica-buildings/Buildings/Fluid/BaseClasses/ActuatorFilter.mo"
  jacobian->tmpVars[25] /* fan.filter.x.$pDERFMIDER.dummyVarFMIDER[1] JACOBIAN_DIFF_VAR */ = ((data->simulationInfo->realParameter[195] /* fan.filter.u_nom PARAM */)) * (jacobian->seedVars[0] /* fan.filter.s.SeedFMIDER[1] SEED_VAR */);
#line 621 OMC_FILE
  TRACE_POP
}

/*
equation index: 963
type: SIMPLE_ASSIGN
$DER.fan.filter.s.$pDERFMIDER.dummyVarFMIDER[1] = (ovePum.SeedFMIDER - fan.filter.x.$pDERFMIDER.dummyVarFMIDER[1]) * fan.filter.w_u
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_963(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 18;
  const int equationIndexes[2] = {1,963};
#line 50 "/home/marius/modelica-buildings/Buildings/Fluid/BaseClasses/ActuatorFilter.mo"
  jacobian->resultVars[0] /* der(fan.filter.s.$pDERFMIDER.dummyVarFMIDER[1]) JACOBIAN_VAR */ = (jacobian->seedVars[6] /* ovePum.SeedFMIDER SEED_VAR */ - jacobian->tmpVars[25] /* fan.filter.x.$pDERFMIDER.dummyVarFMIDER[1] JACOBIAN_DIFF_VAR */) * ((data->simulationInfo->realParameter[197] /* fan.filter.w_u PARAM */));
#line 638 OMC_FILE
  TRACE_POP
}

/*
equation index: 964
type: SIMPLE_ASSIGN
bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER = 4184.0 * $cse1.T.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_964(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 19;
  const int equationIndexes[2] = {1,964};
  jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = (4184.0) * (jacobian->tmpVars[0] /* $cse1.T.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */);
  TRACE_POP
}

/*
equation index: 965
type: SIMPLE_ASSIGN
fluPor.2.forward.T.$pDERFMIDER.dummyVarFMIDER = if fluPor[2].m_flow >= 0.0 then 0.0002390057361376673 * bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER else 0.0
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_965(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 20;
  const int equationIndexes[2] = {1,965};
  modelica_boolean tmp52;
  relationhysteresis(data, &tmp52, (data->localData[0]->realVars[68] /* fluPor[2].m_flow variable */), 0.0, 0, GreaterEq, GreaterEqZC);
  jacobian->resultVars[6] /* fluPor.2.forward.T.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */ = (tmp52?(0.0002390057361376673) * (jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */):0.0);
  TRACE_POP
}

/*
equation index: 966
type: SIMPLE_ASSIGN
hea.outCon.dhAct.$pDERFMIDER.dummyVarFMIDER = smooth(0, if noEvent(hea.outCon.hSet - bou.ports[1].h_outflow > hea.outCon.deltaH) then hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER - bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER else if noEvent(hea.outCon.hSet - bou.ports[1].h_outflow < (-hea.outCon.deltaH)) then 0.0 else if noEvent(hea.outCon.deltaH > 0.0) then 0.25 * ((((hea.outCon.hSet - bou.ports[1].h_outflow) / hea.outCon.deltaH) ^ 2.0 - 3.0) * (bou.ports[1].h_outflow - hea.outCon.hSet) / hea.outCon.deltaH * (hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER - bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER) + ((((hea.outCon.hSet - bou.ports[1].h_outflow) / hea.outCon.deltaH) ^ 2.0 - 3.0) * (bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER - hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER) + 2.0 * (hea.outCon.hSet - bou.ports[1].h_outflow) / hea.outCon.deltaH * (hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER - bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER) * hea.outCon.deltaH / hea.outCon.deltaH ^ 2.0 * (bou.ports[1].h_outflow - hea.outCon.hSet)) * hea.outCon.deltaH / hea.outCon.deltaH ^ 2.0 * (hea.outCon.hSet - bou.ports[1].h_outflow)) + 0.5 * (hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER - bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER) else 0.5 * (hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER - bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER))
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_966(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 21;
  const int equationIndexes[2] = {1,966};
  modelica_boolean tmp53;
  modelica_boolean tmp54;
  modelica_boolean tmp55;
  modelica_real tmp56;
  modelica_real tmp57;
  modelica_real tmp58;
  modelica_real tmp59;
  modelica_boolean tmp60;
  modelica_real tmp61;
  modelica_boolean tmp62;
  modelica_real tmp63;
  modelica_boolean tmp64;
  modelica_real tmp65;
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  tmp53 = Greater((data->localData[0]->realVars[75] /* hea.outCon.hSet variable */) - (data->localData[0]->realVars[24] /* bou.ports[1].h_outflow variable */),(data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */));
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  tmp64 = (modelica_boolean)tmp53;
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  if(tmp64)
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  {
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    tmp65 = jacobian->tmpVars[38] /* hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ - jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */;
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  }
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  else
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  {
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    tmp54 = Less((data->localData[0]->realVars[75] /* hea.outCon.hSet variable */) - (data->localData[0]->realVars[24] /* bou.ports[1].h_outflow variable */),(-(data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */)));
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    tmp62 = (modelica_boolean)tmp54;
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    if(tmp62)
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    {
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      tmp63 = 0.0;
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    }
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    else
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    {
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      tmp55 = Greater((data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */),0.0);
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      tmp60 = (modelica_boolean)tmp55;
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      if(tmp60)
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      {
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp56 = DIVISION((data->localData[0]->realVars[75] /* hea.outCon.hSet variable */) - (data->localData[0]->realVars[24] /* bou.ports[1].h_outflow variable */),(data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */),"hea.outCon.deltaH");
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp57 = DIVISION((data->localData[0]->realVars[75] /* hea.outCon.hSet variable */) - (data->localData[0]->realVars[24] /* bou.ports[1].h_outflow variable */),(data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */),"hea.outCon.deltaH");
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp58 = (data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */);
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp59 = (data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */);
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp61 = (0.25) * ((DIVISION(((tmp56 * tmp56) - 3.0) * ((data->localData[0]->realVars[24] /* bou.ports[1].h_outflow variable */) - (data->localData[0]->realVars[75] /* hea.outCon.hSet variable */)),(data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */),"hea.outCon.deltaH")) * (jacobian->tmpVars[38] /* hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ - jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + (DIVISION((((tmp57 * tmp57) - 3.0) * (jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ - jacobian->tmpVars[38] /* hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + (DIVISION(((2.0) * (DIVISION((data->localData[0]->realVars[75] /* hea.outCon.hSet variable */) - (data->localData[0]->realVars[24] /* bou.ports[1].h_outflow variable */),(data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */),"hea.outCon.deltaH"))) * ((jacobian->tmpVars[38] /* hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ - jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */))),(tmp58 * tmp58),"hea.outCon.deltaH ^ 2.0")) * ((data->localData[0]->realVars[24] /* bou.ports[1].h_outflow variable */) - (data->localData[0]->realVars[75] /* hea.outCon.hSet variable */))) * ((data->simulationInfo->realParameter[313] /* hea.outCon.deltaH PARAM */)),(tmp59 * tmp59),"hea.outCon.deltaH ^ 2.0")) * ((data->localData[0]->realVars[75] /* hea.outCon.hSet variable */) - (data->localData[0]->realVars[24] /* bou.ports[1].h_outflow variable */))) + (0.5) * (jacobian->tmpVars[38] /* hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ - jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */);
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      }
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      else
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      {
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
        tmp61 = (0.5) * (jacobian->tmpVars[38] /* hea.outCon.hSet.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ - jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */);
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      }
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
      tmp63 = tmp61;
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    }
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
    tmp65 = tmp63;
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  }
#line 288 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  jacobian->tmpVars[37] /* hea.outCon.dhAct.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = tmp65;
#line 768 OMC_FILE
  TRACE_POP
}

/*
equation index: 967
type: SIMPLE_ASSIGN
y.$pDERFMIDER.dummyVarFMIDER = hea.outCon.m_flow_pos * hea.outCon.dhAct.$pDERFMIDER.dummyVarFMIDER + hea.outCon.m_flow_pos.$pDERFMIDER.dummyVarFMIDER * hea.outCon.dhAct
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_967(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 22;
  const int equationIndexes[2] = {1,967};
#line 294 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  jacobian->resultVars[9] /* y.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */ = ((data->localData[0]->realVars[80] /* hea.outCon.m_flow_pos variable */)) * (jacobian->tmpVars[37] /* hea.outCon.dhAct.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + (jacobian->tmpVars[42] /* hea.outCon.m_flow_pos.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->localData[0]->realVars[73] /* hea.outCon.dhAct variable */));
#line 785 OMC_FILE
  TRACE_POP
}

/*
equation index: 968
type: SIMPLE_ASSIGN
hea.port_a.h_outflow.$pDERFMIDER.dummyVarFMIDER = bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER + hea.outCon.dhAct.$pDERFMIDER.dummyVarFMIDER
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_968(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 23;
  const int equationIndexes[2] = {1,968};
#line 293 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/PrescribedOutlet.mo"
  jacobian->tmpVars[43] /* hea.port_a.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = jacobian->tmpVars[15] /* bou.ports.1.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ + jacobian->tmpVars[37] /* hea.outCon.dhAct.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */;
#line 802 OMC_FILE
  TRACE_POP
}

/*
equation index: 969
type: SIMPLE_ASSIGN
resSup.port_b.h_outflow.$pDERFMIDER.dummyVarFMIDER = hea.port_a.h_outflow.$pDERFMIDER.dummyVarFMIDER + fan.prePow.Q_flow * fan.vol.steBal.m_flowInv.$pDERFMIDER.dummyVarFMIDER + fan.prePow.Q_flow.$pDERFMIDER.dummyVarFMIDER * fan.vol.steBal.m_flowInv
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_969(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 24;
  const int equationIndexes[2] = {1,969};
#line 209 "/home/marius/modelica-buildings/Buildings/Fluid/Interfaces/StaticTwoPortConservationEquation.mo"
  jacobian->tmpVars[50] /* resSup.port_b.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ = jacobian->tmpVars[43] /* hea.port_a.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */ + ((data->localData[0]->realVars[46] /* fan.prePow.Q_flow variable */)) * (jacobian->tmpVars[35] /* fan.vol.steBal.m_flowInv.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) + (jacobian->tmpVars[32] /* fan.prePow.Q_flow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */) * ((data->localData[0]->realVars[61] /* fan.vol.steBal.m_flowInv variable */));
#line 819 OMC_FILE
  TRACE_POP
}

/*
equation index: 970
type: SIMPLE_ASSIGN
fluPor.1.forward.T.$pDERFMIDER.dummyVarFMIDER = if fluPor[1].m_flow >= 0.0 then 0.0002390057361376673 * resSup.port_b.h_outflow.$pDERFMIDER.dummyVarFMIDER else 0.0
*/
void Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_970(DATA *data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  const int baseClockIndex = 0;
  const int subClockIndex = 25;
  const int equationIndexes[2] = {1,970};
  modelica_boolean tmp66;
  relationhysteresis(data, &tmp66, (data->localData[0]->realVars[67] /* fluPor[1].m_flow variable */), 0.0, 1, GreaterEq, GreaterEqZC);
  jacobian->resultVars[5] /* fluPor.1.forward.T.$pDERFMIDER.dummyVarFMIDER JACOBIAN_VAR */ = (tmp66?(0.0002390057361376673) * (jacobian->tmpVars[50] /* resSup.port_b.h_outflow.$pDERFMIDER.dummyVarFMIDER JACOBIAN_DIFF_VAR */):0.0);
  TRACE_POP
}

OMC_DISABLE_OPT
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacFMIDER_constantEqns(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH

  int index = Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_INDEX_JAC_FMIDER;
  
  
  TRACE_POP
  return 0;
}

int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacFMIDER_column(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH

  int index = Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_INDEX_JAC_FMIDER;
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_945(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_946(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_947(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_948(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_949(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_950(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_951(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_952(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_953(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_954(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_955(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_956(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_957(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_958(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_959(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_960(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_961(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_962(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_963(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_964(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_965(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_966(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_967(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_968(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_969(data, threadData, jacobian, parentJacobian);
  Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_eqFunction_970(data, threadData, jacobian, parentJacobian);
  TRACE_POP
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacH_column(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  TRACE_POP
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacF_column(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  TRACE_POP
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacD_column(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  TRACE_POP
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacC_column(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  TRACE_POP
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacB_column(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH
  TRACE_POP
  return 0;
}
/* constant equations */
/* dynamic equations */

OMC_DISABLE_OPT
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacA_constantEqns(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH

  int index = Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_INDEX_JAC_A;
  
  
  TRACE_POP
  return 0;
}

int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_functionJacA_column(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian, ANALYTIC_JACOBIAN *parentJacobian)
{
  TRACE_PUSH

  int index = Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_INDEX_JAC_A;
  TRACE_POP
  return 0;
}

OMC_DISABLE_OPT
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_initialAnalyticJacobianFMIDER(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian)
{
  TRACE_PUSH
  size_t count;

  FILE* pFile = openSparsePatternFile(data, threadData, "Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_JacFMIDER.bin");
  
  initAnalyticJacobian(jacobian, 7, 10, 61, NULL, jacobian->sparsePattern);
  jacobian->sparsePattern = allocSparsePattern(7, 11, 2);
  jacobian->availability = JACOBIAN_AVAILABLE;
  
  /* read lead index of compressed sparse column */
  count = omc_fread(jacobian->sparsePattern->leadindex, sizeof(unsigned int), 7+1, pFile, FALSE);
  if (count != 7+1) {
    throwStreamPrint(threadData, "Error while reading lead index list of sparsity pattern. Expected %d, got %ld", 7+1, count);
  }
  
  /* read sparse index */
  count = omc_fread(jacobian->sparsePattern->index, sizeof(unsigned int), 11, pFile, FALSE);
  if (count != 11) {
    throwStreamPrint(threadData, "Error while reading row index list of sparsity pattern. Expected %d, got %ld", 7+1, count);
  }
  
  /* write color array */
  /* color 1 with 2 columns */
  readSparsePatternColor(threadData, pFile, jacobian->sparsePattern->colorCols, 1, 2);
  /* color 2 with 5 columns */
  readSparsePatternColor(threadData, pFile, jacobian->sparsePattern->colorCols, 2, 5);
  
  omc_fclose(pFile);
  
  TRACE_POP
  return 0;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_initialAnalyticJacobianH(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian)
{
  TRACE_PUSH
  TRACE_POP
  jacobian->availability = JACOBIAN_NOT_AVAILABLE;
  return 1;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_initialAnalyticJacobianF(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian)
{
  TRACE_PUSH
  TRACE_POP
  jacobian->availability = JACOBIAN_NOT_AVAILABLE;
  return 1;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_initialAnalyticJacobianD(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian)
{
  TRACE_PUSH
  TRACE_POP
  jacobian->availability = JACOBIAN_NOT_AVAILABLE;
  return 1;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_initialAnalyticJacobianC(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian)
{
  TRACE_PUSH
  TRACE_POP
  jacobian->availability = JACOBIAN_NOT_AVAILABLE;
  return 1;
}
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_initialAnalyticJacobianB(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian)
{
  TRACE_PUSH
  TRACE_POP
  jacobian->availability = JACOBIAN_NOT_AVAILABLE;
  return 1;
}
OMC_DISABLE_OPT
int Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_initialAnalyticJacobianA(DATA* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian)
{
  TRACE_PUSH
  size_t count;

  FILE* pFile = openSparsePatternFile(data, threadData, "Buildings_Fluid_FMI_ExportContainers_Examples_FMUs_PumpCircuit_JacA.bin");
  
  initAnalyticJacobian(jacobian, 2, 2, 0, NULL, jacobian->sparsePattern);
  jacobian->sparsePattern = allocSparsePattern(2, 3, 2);
  jacobian->availability = JACOBIAN_ONLY_SPARSITY;
  
  /* read lead index of compressed sparse column */
  count = omc_fread(jacobian->sparsePattern->leadindex, sizeof(unsigned int), 2+1, pFile, FALSE);
  if (count != 2+1) {
    throwStreamPrint(threadData, "Error while reading lead index list of sparsity pattern. Expected %d, got %ld", 2+1, count);
  }
  
  /* read sparse index */
  count = omc_fread(jacobian->sparsePattern->index, sizeof(unsigned int), 3, pFile, FALSE);
  if (count != 3) {
    throwStreamPrint(threadData, "Error while reading row index list of sparsity pattern. Expected %d, got %ld", 2+1, count);
  }
  
  /* write color array */
  /* color 1 with 1 columns */
  readSparsePatternColor(threadData, pFile, jacobian->sparsePattern->colorCols, 1, 1);
  /* color 2 with 1 columns */
  readSparsePatternColor(threadData, pFile, jacobian->sparsePattern->colorCols, 2, 1);
  
  omc_fclose(pFile);
  
  TRACE_POP
  return 0;
}



