# Scripts for interaction with Treasure PostgreSQL database

This library contains example scripts and functions for interaction with the database. 

It is recommended to copy the scripts to a separate folder before altering them. Personal changes should not be pushed to the repository.

For the scripts to work, the folder where the buildings repository is located must be in your PYTHONPATH

All scripts that interact with the database needs authentication. To enable this, the user variable

To get access to the database please contact: [harald.walnum@sintef.no]

## db_export_data.py

This script shows how to export datafiles from the database. As default, the script reads the `filter.json` to create metadata filter. This require this file to be in the same folder. See below for more details on filter possibilities

The export function (`treaSQL.export_data()`)  have the following optional inputs: 

- `export directory` (string): Relative path to store export files. If not set, data is not stored, and only returned as variables.

- `metadata` (dictionary): Filter to select wanted buildings. It is possible to filter on all building metadata 

- `overwrite` (boolean): If `False`, the function will look for data in the export folder and only export buildings that are not already there. If `True`, all buildings matching the filter will be exported and existing files will be overwritten. *Default is* `False`

- `force_export` (boolean): If `False`, the user will be informed on how many datasets that will be exported and asked if it should continue. If `True` data is exported with out confirmation. Default is `False`

Returns:

If answer `Y` to continue to export or `force_export = True` the function returns a dictionary with building data sorted on building_id

Else, the function returns a list of building_ids matching the filter.

### Filter options

For $string$ fields only sting inputs are valid. For $integer$ fields, both $string$ and `integer` are valid. 

In general, inputs are interpreted according to the following rules (and in the given order):

- If the input value is $integer$, the field must be equal to integer value

- For string inputs, the following options are possibel, but only one of them per metadata type:
  
  - RANGE: (integer fields only): Will return all buildings where the field is within the range, including boundaries. E.g. `{floor_area: "1000-2000"}` will return all buildings with floor area between 1000 and 2000 $m^2$
  
  - LIST + separated : Will return buildings where all listed value are present in the field. E.g. `{sh_heat_source: "EH+EFH"}` will return all buildings that have *both* EH (electric heater) and EFH (electric floor heating) as space heating source
  
  - LIST , separated : Will return buildings where all listed value are present in the field. E.g. `{sh_heat_source: "EH,EFH"}` will return all buildings that have *any of* EH (electric heater) and/or EFH (electric floor heating) as space heating source. {sh_heat_source: "EH,"} will return all buildings that has EH as only space heating source or in combination with any other heat sources.
  
  - EXACT MATCH: If none of the above separators are present, the input is interpreted as a single value input that requires exact match with the field. E.g. `{sh_heat_source: "EH"}` will return all buildings that have *only* EH (electric heater) as space heating source.

Below the filtering options are listed, with a short description of possible inputs.
```yaml
{
    "file_owner": string,
    "data_source": string,
    "building_name": string,
    "location": string,
    "weather_data": string,
    "year_of_construction": integer,
    "floor_area": integer,
    "heated_floor_area": integer,
    "number_of_users": integer,
    "number_of_units": integer,
    "number_of_buildings": integer,
    "building_category": string,  #  ['Hou', 'Apt', 'Off', 'Shp', 'Htl', 'Kdg', 'Sch', 'Uni', 'CuS', 'Nsh', 'Hos'])
    "energy_eff_standard": string,  # ['Reg', 'Eff', 'Vef'])
    "energy_label": string, # ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    "notes": string,
    "influenced": integer,  # [0,1,2] 2 = Unknown
    "central_heating_system": integer, # [0,1,2] 2 = Unknown
    "dhw_heat_source": string,  #  see: *buildings/resources/heat_sources.csv*
    "sh_heat_source": string, #  see: *buildings/resources/heat_sources.csv*
    "ventilation_heat_source":# see: *buildings/resources/heat_sources.csv*
    "snow_melt_heat_source": string, # see: *buildings/resources/heat_sources.csv*
    "cooling_source": string, # see: *buildings/resources/cooling_sources.csv*
    "ventilation_types": string, # see: *buildings/resources/ventilation_types.csv*
    "ev_chargepoints": null,  # Not available
    "pv": null,  # Not available
    "battery": null,  # Not available
    "night_setback": integer, # [0,1,2] 2 = Unknown
    "lighting_control": integer, #  [0,1,2] 2 = Unknown
    "control_description": string
}
```
