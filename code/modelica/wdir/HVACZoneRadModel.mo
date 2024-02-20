model HVACZoneRadModel "Declaration of an FMU that exports a simple convective only HVAC system"
  replaceable package MediumA = Buildings.Media.Air "Medium for air";
  replaceable package MediumW = Buildings.Media.Water "Medium for water";
  parameter Boolean allowFlowReversal = false "= true to allow flow reversal, false restricts to design direction (inlet -> outlet)" annotation(
    Dialog(tab = "Assumptions"),
    Evaluate = true);
  //////////////////////////////////////////////////////////
  // Heat recovery effectiveness
  parameter Real eps = 0.8 "Heat recovery effectiveness";
  /////////////////////////////////////////////////////////
  // Design air conditions
  parameter Modelica.Units.SI.Temperature TASup_nominal = 291.15 "Nominal air temperature supplied to room";
  parameter Modelica.Units.SI.DimensionlessRatio wASup_nominal = 0.012 "Nominal air humidity ratio supplied to room [kg/kg] assuming 90% relative humidity";
  parameter Modelica.Units.SI.Temperature TRooSet = 297.15 "Nominal room air temperature";
  parameter Modelica.Units.SI.Temperature TOut_nominal = 303.15 "Design outlet air temperature";
  parameter Modelica.Units.SI.Temperature THeaRecLvg = TOut_nominal - eps*(TOut_nominal - TRooSet) "Air temperature leaving the heat recovery";
  parameter Modelica.Units.SI.DimensionlessRatio wHeaRecLvg = 0.0135 "Air humidity ratio leaving the heat recovery [kg/kg]";
  /////////////////////////////////////////////////////////
  // Cooling loads and air mass flow rates
  parameter Real UA(unit = "W/K") = 10E3 "Average UA-value of the room";
  parameter Modelica.Units.SI.HeatFlowRate QRooInt_flow = 1000 "Internal heat gains of the room";
  parameter Modelica.Units.SI.HeatFlowRate QRooC_flow_nominal = -QRooInt_flow - UA/30*(TOut_nominal - TRooSet) "Nominal cooling load of the room";
  parameter Modelica.Units.SI.MassFlowRate mA_flow_nominal = 1.3*QRooC_flow_nominal/1006/(TASup_nominal - TRooSet) "Nominal air mass flow rate, increased by factor 1.3 to allow for recovery after temperature setback";
  parameter Modelica.Units.SI.TemperatureDifference dTFan = 2 "Estimated temperature raise across fan that needs to be made up by the cooling coil";
  parameter Modelica.Units.SI.HeatFlowRate QCoiC_flow_nominal = mA_flow_nominal*(TASup_nominal - THeaRecLvg - dTFan)*1006 + mA_flow_nominal*(wASup_nominal - wHeaRecLvg)*2458.3e3 "Cooling load of coil, taking into account outside air sensible and latent heat removal";
  /////////////////////////////////////////////////////////
  // Water temperatures and mass flow rates
  parameter Modelica.Units.SI.Temperature TWSup_nominal = 285.15 "Water supply temperature";
  parameter Modelica.Units.SI.Temperature TWRet_nominal = 289.15 "Water return temperature";
  parameter Modelica.Units.SI.MassFlowRate m_flow_nominal = -QCoiC_flow_nominal/(TWRet_nominal - TWSup_nominal)/4200 "Nominal water mass flow rate";
  /////////////////////////////////////////////////////////
  // HVAC models
  Buildings.Fluid.Movers.FlowControlled_m_flow pump(redeclare package Medium = MediumW, allowFlowReversal = false, energyDynamics = Modelica.Fluid.Types.Dynamics.FixedInitial, m_flow_nominal = m_flow_nominal, nominalValuesDefineDefaultPressureCurve = true, use_inputFilter = false) annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{40, 20}, {60, 40}}, rotation = 0)));
  Buildings.Fluid.Actuators.Valves.ThreeWayLinear val(redeclare package Medium = MediumW, dpValve_nominal = 1000, energyDynamics = Modelica.Fluid.Types.Dynamics.SteadyState, l = {0.002, 0.002}, m_flow_nominal = m_flow_nominal, portFlowDirection_1 = Modelica.Fluid.Types.PortFlowDirection.Entering, portFlowDirection_2 = Modelica.Fluid.Types.PortFlowDirection.Leaving, portFlowDirection_3 = Modelica.Fluid.Types.PortFlowDirection.Entering, use_inputFilter = false) annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{10, 20}, {30, 40}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT bou(nPorts = 1, redeclare package Medium = MediumW) annotation(
    Placement(visible = true, transformation(origin = {-50, 20}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Gain gain(k = m_flow_nominal) annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{0, 70}, {20, 90}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.PressureDrop res(redeclare package Medium = MediumW, dp_nominal = 100, m_flow_nominal = 0.2) annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{70, 20}, {90, 40}}, rotation = 0)));
  Buildings.Fluid.HeatExchangers.Heater_T hea(redeclare package Medium = MediumW, dp_nominal = 100, m_flow_nominal = 0.2) annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{-20, 20}, {0, 40}}, rotation = 0)));
  Buildings.Fluid.HeatExchangers.Radiators.RadiatorEN442_2 rad(redeclare package Medium = MediumW, Q_flow_nominal = 4000, T_a_nominal = 333.15, T_b_nominal = 313.15, m_flow_nominal = 0.2) annotation(
    Placement(visible = true, transformation(origin = {127, 17}, extent = {{-15, -15}, {15, 15}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput Tsup annotation(
    Placement(visible = true, transformation(origin = {-166, 58}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-144, 72}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput m_flow annotation(
    Placement(visible = true, transformation(origin = {-166, 122}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-146, 128}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput val_ope annotation(
    Placement(visible = true, transformation(origin = {-166, 94}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-154, 104}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Sensors.HeatFlowSensor heatFlowSensor annotation(
    Placement(visible = true, transformation(origin = {160, 122}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Sensors.HeatFlowSensor heatFlowSensor1 annotation(
    Placement(visible = true, transformation(origin = {160, 90}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
    Placement(visible = true, transformation(origin = {190, 110}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {190, 110}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput y1 annotation(
    Placement(visible = true, transformation(origin = {194, 68}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {198, 64}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(bou.ports[1], hea.port_a) annotation(
    Line(points = {{-40, 20}, {-20, 20}, {-20, 30}}, color = {0, 127, 255}));
  connect(hea.port_b, val.port_1) annotation(
    Line(points = {{0, 30}, {10, 30}}, color = {0, 127, 255}));
  connect(val.port_2, pump.port_a) annotation(
    Line(points = {{30, 30}, {40, 30}}, color = {0, 127, 255}));
  connect(gain.y, pump.m_flow_in) annotation(
    Line(points = {{22, 80}, {50, 80}, {50, 42}}, color = {0, 0, 127}));
  connect(pump.port_b, res.port_a) annotation(
    Line(points = {{60, 30}, {70, 30}}, color = {0, 127, 255}));
  connect(res.port_b, rad.port_a) annotation(
    Line(points = {{90, 30}, {90, 17}, {112, 17}}, color = {0, 127, 255}));
  connect(rad.port_b, val.port_3) annotation(
    Line(points = {{142, 17}, {142, -20}, {20, -20}, {20, 20}}));
  connect(hea.TSet, Tsup) annotation(
    Line(points = {{-22, 38}, {-124, 38}, {-124, 58}, {-166, 58}}, color = {0, 0, 127}));
  connect(gain.u, m_flow) annotation(
    Line(points = {{-2, 80}, {-96, 80}, {-96, 122}, {-166, 122}}, color = {0, 0, 127}));
  connect(val.y, val_ope) annotation(
    Line(points = {{20, 42}, {20, 52}, {-112, 52}, {-112, 94}, {-166, 94}}, color = {0, 0, 127}));
  connect(rad.heatPortCon, heatFlowSensor.port_a) annotation(
    Line(points = {{124, 28}, {109, 28}, {109, 56}, {118, 56}, {118, 122}, {150, 122}}, color = {191, 0, 0}));
  connect(rad.heatPortRad, heatFlowSensor1.port_a) annotation(
    Line(points = {{130, 28}, {130, 90}, {150, 90}}, color = {191, 0, 0}));
  connect(heatFlowSensor.Q_flow, y) annotation(
    Line(points = {{160, 112}, {172, 112}, {172, 110}, {190, 110}}, color = {0, 0, 127}));
  connect(heatFlowSensor1.Q_flow, y1) annotation(
    Line(points = {{160, 80}, {176, 80}, {176, 68}, {194, 68}}, color = {0, 0, 127}));
  annotation(
    Icon(coordinateSystem(preserveAspectRatio = false, extent = {{-160, -160}, {160, 160}}), graphics = {Text(textColor = {0, 0, 127}, extent = {{-24, -132}, {26, -152}}, textString = "TOut")}),
    Diagram(coordinateSystem(preserveAspectRatio = false, extent = {{-160, -160}, {160, 160}})),
    Documentation(info = "<html>
<p>
This example demonstrates how to export a model of an HVAC system
that only provides convective cooling to a single thermal zone.
The HVAC system is adapted from
<a href=\"modelica://Buildings.Examples.Tutorial.SpaceCooling.System3\">
Buildings.Examples.Tutorial.SpaceCooling.System3</a>,
but flow resistances have been added to have the same configuration as
<a href=\"modelica://Buildings.Fluid.FMI.ExportContainers.Examples.FMUs.HVACZones\">
Buildings.Fluid.FMI.ExportContainers.Examples.FMUs.HVACZones</a>.
Having the same configuration is needed for the validation test
<a href=\"modelica://Buildings.Fluid.FMI.ExportContainers.Validation.RoomHVAC\">
Buildings.Fluid.FMI.ExportContainers.Validation.RoomHVAC</a>.
</p>
<p>
The example extends from
<a href=\"modelica://Buildings.Fluid.FMI.ExportContainers.HVACZone\">
Buildings.Fluid.FMI.ExportContainers.HVACZone
</a>
which provides the input and output signals that are needed to interface
the acausal HVAC system model with causal connectors of FMI.
The instance <code>hvacAda</code> is the HVAC adapter
that contains on the left a fluid port, and on the right signal ports
which are then used to connect at the top-level of the model to signal
ports which are exposed at the FMU interface.
</p>
</html>", revisions = "<html>
<ul>
<li>
September 21, 2021 by David Blum:<br/>
Correct supply and return water parameterization.<br/>
Use explicit calculation of sensible and latent load to determine design load
on cooling coil.<br/>
This is for <a href=\"https://github.com/lbl-srg/modelica-buildings/issues/2624\">#2624</a>.
</li>
<li>
May 15, 2019, by Jianjun Hu:<br/>
Replaced fluid source. This is for
<a href=\"https://github.com/ibpsa/modelica-ibpsa/issues/1072\"> #1072</a>.
</li>
<li>
November 11, 2016, by Michael Wetter:<br/>
Made the cooling coil replaceable because the Buildings library
uses the model for validation with a cooling coil model that is not
in the Annex 60 library.
</li>
<li>
April 16, 2016 by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"),
    __Dymola_Commands(file = "modelica://Buildings/Resources/Scripts/Dymola/Fluid/FMI/ExportContainers/Examples/FMUs/HVACZone.mos" "Export FMU"),
    uses(Modelica(version = "4.0.0"), Buildings(version = "10.0.0")));
end HVACZoneRadModel;