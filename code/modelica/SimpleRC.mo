within ;
model SimpleRC
  "A simple thermal R1C1 model with sinusoidal outside air temperature and a feedback controlled heater."
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor cap(C=1e6)
    "Thermal capacitance of room"
    annotation (Placement(transformation(extent={{30,0},{50,20}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalResistor res(R=0.01)
    "Thermal resistance to outside"
    annotation (Placement(transformation(extent={{0,-10},{20,10}})));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor senTZone
    "Room air temperature sensor"
    annotation (Placement(transformation(extent={{60,-10},{80,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature preTOut
    "Set the outside air temperature"
    annotation (Placement(transformation(extent={{-40,-10},{-20,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
    "Set the heating power to the room"
    annotation (Placement(transformation(extent={{0,-40},{20,-20}})));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
    Placement(transformation(origin = {104, 28}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {104, 28}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealInput phi_h annotation(
    Placement(transformation(origin = {-106, 56}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-98, 54}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Interfaces.RealInput Ta annotation(
    Placement(transformation(origin = {-104, -32}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-106, 56}, extent = {{-20, -20}, {20, 20}})));
equation
  connect(res.port_b, cap.port) annotation(
    Line(points = {{20, 0}, {40, 0}}, color = {191, 0, 0}));
  connect(cap.port, senTZone.port) annotation(
    Line(points = {{40, 0}, {60, 0}}, color = {191, 0, 0}));
  connect(preTOut.port, res.port_a) annotation(
    Line(points = {{-20, 0}, {0, 0}}, color = {191, 0, 0}));
  connect(preHeat.port, cap.port) annotation(
    Line(points = {{20, -30}, {40, -30}, {40, 0}}, color = {191, 0, 0}));
  connect(senTZone.T, y) annotation(
    Line(points = {{80, 0}, {80, 28}, {104, 28}}, color = {0, 0, 127}));
  connect(phi_h, preHeat.Q_flow) annotation(
    Line(points = {{-106, 56}, {-62, 56}, {-62, -30}, {0, -30}}, color = {0, 0, 127}));
  connect(Ta, preTOut.T) annotation(
    Line(points = {{-104, -32}, {-72, -32}, {-72, 0}, {-42, 0}}, color = {0, 0, 127}));
  annotation (uses(Modelica(version="3.2.3"),
      Buildings(version="8.0.0")),
      experiment(
      StopTime=60,
      Interval=1,
      Tolerance=1e-06));
end SimpleRC;