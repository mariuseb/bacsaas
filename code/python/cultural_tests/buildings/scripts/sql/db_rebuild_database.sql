-- enter these SQL commands to completely wipe the database
-- all tables are deleted and created from scratch

DROP TABLE IF EXISTS buildings;
CREATE TABLE buildings (
	id SERIAL PRIMARY KEY,
	file_owner TEXT,
	data_source TEXT,
	last_update TIMESTAMP WITH TIME ZONE,
	building_name TEXT,
	location TEXT,
	weather_data TEXT,
	year_of_construction INTEGER,
	floor_area INTEGER,
	heated_floor_area INTEGER,	
	number_of_users INTEGER,
	number_of_units INTEGER,
	number_of_buildings INTEGER,
	building_category TEXT,
	energy_eff_standard TEXT,
	energy_label TEXT,
	notes TEXT,
	influenced INTEGER,
	central_heating_system INTEGER,
	dhw_heat_source TEXT,
	sh_heat_source TEXT,
	ventilation_heat_source TEXT,
	snow_melt_heat_source TEXT,
	cooling_source TEXT,
	ventilation_types TEXT,
	ev_chargepoints TEXT,
	pv TEXT,
	battery TEXT,
	night_setback INTEGER,
	lighting_control INTEGER,
	control_description TEXT,
	timestamp_format TEXT,
	time_zone TEXT
);


DROP TABLE IF EXISTS timeseries;
CREATE TABLE timeseries (
	id SERIAL PRIMARY KEY,
	building INTEGER,
	timestamp_from TIMESTAMP WITH TIME ZONE,
	timestamp_to TIMESTAMP WITH TIME ZONE,
	resolution INTEGER,
	measurement_types TEXT,
	data BYTEA
);

-- grant access rights

GRANT ALL ON TABLE public.buildings TO "bjornlu@sintef.no";
GRANT ALL ON TABLE public.buildings TO "hwaln@sintef.no" WITH GRANT OPTION;
GRANT SELECT ON TABLE public.buildings TO "ases@sintef.no";
GRANT SELECT ON TABLE public.buildings TO "benjamind@sintef.no";
GRANT SELECT ON TABLE public.buildings TO "synnel@sintef.no";

GRANT ALL ON TABLE public.timeseries TO "bjornlu@sintef.no";
GRANT ALL ON TABLE public.timeseries TO "hwaln@sintef.no" WITH GRANT OPTION;
GRANT SELECT ON TABLE public.timeseries TO "ases@sintef.no";
GRANT SELECT ON TABLE public.timeseries TO "benjamind@sintef.no";
GRANT SELECT ON TABLE public.timeseries TO "synnel@sintef.no";

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public to "hwaln@sintef.no" WITH GRANT OPTION;

-- info about choice of bytea format for timeseries:
-- https://wiki.postgresql.org/wiki/BinaryFilesInDB