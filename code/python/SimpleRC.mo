within ;
model Simple2R2C
  "A simple thermal R1C1 model with sinusoidal outside air temperature and a feedback controlled heater."
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor Ci(C=1e6)
    "Thermal capacitance of room"
    annotation (Placement(transformation(extent={{30,0},{50,20}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalResistor Rea(R=0.01)
    "Thermal resistance to outside"
    annotation (Placement(visible = true, transformation(origin = {-58, 0}, extent = {{0, -10}, {20, 10}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor senTZone
    "Room air temperature sensor"
    annotation (Placement(transformation(extent={{60,-10},{80,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature preTOut
    "Set the outside air temperature"
    annotation (Placement(visible = true, transformation(origin = {-44, 0}, extent = {{-40, -10}, {-20, 10}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
    "Set the heating power to the room"
    annotation (Placement(transformation(extent={{0,-40},{20,-20}})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor Ce(C = 5e6) annotation(
    Placement(visible = true, transformation(origin = {-54, 0}, extent = {{30, 0}, {50, 20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.ThermalResistor Rie(R = 0.01) annotation(
    Placement(visible = true, transformation(origin = {4, 0}, extent = {{0, -10}, {20, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput phi_h annotation(
    Placement(visible = true, transformation(origin = {-108, 74}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-90, 66}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput Ta annotation(
    Placement(visible = true, transformation(origin = {-110, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-90, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput TZone annotation(
    Placement(visible = true, transformation(origin = {111, 1}, extent = {{-15, -15}, {15, 15}}, rotation = 0), iconTransformation(origin = {106, -16}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput phi_s annotation(
    Placement(visible = true, transformation(origin = {-110, -78}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-94, -66}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Math.Gain Ai(k = 0)  annotation(
    Placement(visible = true, transformation(origin = {20, -78}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow prescribedHeatFlow annotation(
    Placement(visible = true, transformation(origin = {46, -48}, extent = {{0, -40}, {20, -20}}, rotation = 0)));
equation
  connect(Ci.port, senTZone.port) annotation(
    Line(points = {{40, 0}, {60, 0}}, color = {191, 0, 0}));
  connect(preTOut.port, Rea.port_a) annotation(
    Line(points = {{-64, 0}, {-58, 0}}, color = {191, 0, 0}, pattern = LinePattern.Solid));
  connect(preHeat.port, Ci.port) annotation(
    Line(points = {{20, -30}, {40, -30}, {40, 0}}, color = {191, 0, 0}));
  connect(Rea.port_b, Ce.port) annotation(
    Line(points = {{-38, 0}, {-14, 0}}, color = {191, 0, 0}, pattern = LinePattern.Solid));
  connect(Rie.port_a, Ce.port) annotation(
    Line(points = {{4, 0}, {-14, 0}}, color = {191, 0, 0}, pattern = LinePattern.Solid));
  connect(Rie.port_b, Ci.port) annotation(
    Line(points = {{24, 0}, {40, 0}}, color = {191, 0, 0}, pattern = LinePattern.Solid));
  connect(preTOut.T, Ta) annotation(
    Line(points = {{-86, 0}, {-110, 0}}, color = {0, 0, 127}, pattern = LinePattern.Solid));
  connect(preHeat.Q_flow, phi_h) annotation(
    Line(points = {{0, -30}, {-53, -30}, {-53, 74}, {-108, 74}}, color = {0, 0, 127}, pattern = LinePattern.Solid));
  connect(senTZone.T, TZone) annotation(
    Line(points = {{80, 0}, {96, 0}, {96, 1}, {111, 1}}, color = {0, 0, 127}, pattern = LinePattern.Solid));
  connect(phi_s, Ai.u) annotation(
    Line(points = {{-110, -78}, {8, -78}}, color = {0, 0, 127}, pattern = LinePattern.Solid));
  connect(Ai.y, prescribedHeatFlow.Q_flow) annotation(
    Line(points = {{32, -78}, {46, -78}}, color = {0, 0, 127}, pattern = LinePattern.Solid));
  connect(prescribedHeatFlow.port, Ci.port) annotation(
    Line(points = {{66, -78}, {80, -78}, {80, -48}, {50, -48}, {50, 0}, {40, 0}}, color = {191, 0, 0}, pattern = LinePattern.Solid));
  annotation (uses(Modelica(version="3.2.3"),
      Buildings(version="8.0.0")),
      experiment(
      StopTime=60,
      Interval=1,
      Tolerance=1e-06));
end Simple2R2C;