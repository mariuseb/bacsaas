"""
Functions to communicate with PostgreSQL database, as used in the COFACTOR project.
-----------------------------------------------------------------------------------

The following functions are the main interface to the database provided by this module:

* get_creditentials - Get creditentials to logg into. Input is db username (<short_name@sintef.no>)

* check_logfiles - Check logfiles for problems before import.
                Reports back with a dictionary containing number of errors, a full log,
                and lists of errors/warnings.

* write_log_to_file - Write the log(s) returned from check_logfiles to file(s).
                      Not required for import, but useful if errors are encountered.

* import_data - Import files previously checked with check_files to the database.

* export_data - Export data from the database. Expects a date range and a dictionary of
                metadata.

Internal helper functions:
--------------------------

Internal functions are prefixed db_. They are not intended to be called directly by end users.

* db_get_id - Look up a single id on a piece of metadata.

* db_get_metadata - Retrieve entire tables of metadata.

* db_insert - Inserts data to the database.

* db_insert_metadata - Inserts data from the .csv files in /resources/ to the database. Only
                       done once, or when metadata/categories change.

                       2023-02-01: Can probably be retired, since we are reading .csv from
                                   /resources and not from database anymore.

* db_select - Retrieves data from database.

* db_wipe_table - Deletes all data in a table. Use with caution.

"""

import csv
import datetime
import os
import sys

import pandas as pd
from progress.bar import Bar
import psycopg
from psycopg.rows import dict_row

# from . import database_credentials as dbc
from . import treaData
from . import utility_functions as b_utils

accepted_unknowns = ["-", "nan", "Ukn", "Unknown", "", "#I/T", "#N/A", None]
metadata_categorical_lists = [
    "cooling_source",
    "dhw_heat_source",
    "sh_heat_source",
    "ventilation_heat_source",
    "snow_melt_heat_source",
    "ventilation_types",
]

cred = None


def get_credentials(user):
    host = "postgres.sintef.no"
    dbname = "cofactor"

    return f"host={host} dbname={dbname} user={user}"


def check_credentials():
    if cred is None:
        raise Exception("ERROR: Credentials not set")


def check_logfiles(files: list[str] = None, directory: str = None, filetype: str = ".txt"):
    """
    Check if logfiles contain all required fields and may be imported to the database.

    # Arguments:
    * files (list of strings, default None) - list of filenames with full path
    * directory (string, default None) - if provided, ignore files argument and instead
        look for files in this directory
    * filetype (string, default ".txt") - only look at files with this extension

    # Returns a dictionary containing:
    * errors (list of strings) - Error messages.
    * errors_num (integer) - Number of files missing required fields. 0 if all files are okay.
    * errors_files (list of strings) - List of the filenames with errors.
    * warnings (list of strings) - Warning messages.
    * warnings_num (integer) - Number of files missing non-required fields.
    * warnings_files (list of strings) - List of filenames with warnings.
    * checked_num (integer) - Number of files checked.
    * checked_files (list of strings) - List of all files checked.
    * log - A list of all actions taken, including warnings and errors.

    If errors_num == 0, all files in checked_files may be safely imported.

    """

    # abort if no files or directory are supplied
    if files is None and directory is None:
        print("Error: no files or directory in function call, aborting")
        return

    # set up dictionary to gather return values in
    ret = dict()
    ret["errors"] = []
    ret["errors_num"] = 0
    ret["errors_files"] = []
    ret["warnings"] = []
    ret["warnings_num"] = 0
    ret["warnings_files"] = []
    ret["log"] = []

    # ---
    # get filenames
    # ---

    # if directory is provided, ignore files argument and instead scan directory for files
    if directory is not None:
        original_directory = os.getcwd()
        os.chdir(directory)
        files = os.listdir()

    # filter files by filetype
    files_to_check = []
    for file in files:
        if file[-4:] == filetype:
            files_to_check.append(file)

    ret["checked_num"] = len(files_to_check)
    ret["checked_files"] = files_to_check

    # ---
    # check file metadata vs list of required metadata
    # ---

    # --- build dictionary with metadata keys and allowed values for those keys

    ret["log"].append("INFO: --- reading metadata from .csv files in resources/ folder ---")

    metadata = {}
    resource_files = [
        "building_categories",
        "cooling_sources",
        "heat_sources",
        "energy_eff_standards",
        "pv_locations",
        "ventilation_types",
    ]

    for resource_file in resource_files:

        # calling os.path.dirname twice to go to parent directory of __file__
        filename = f"{os.path.dirname(os.path.dirname(__file__))}\\resources\\{resource_file}.csv"

        ret["log"].append(f"INFO: reading allowed metadata values from resource file '{resource_file}.csv'")

        metadata[resource_file] = list(pd.read_csv(filename, sep=";")["description_short"])

        ret["log"].append(f"INFO: allowed values for '{resource_file}', 'description_short':")
        ret["log"].append(f"INFO: {metadata[resource_file]}")

        # allow blank entry (will be replaced with Ukn during import)
        metadata[resource_file].append("")

    # --- start scanning log files

    ret["log"].append("INFO: --- starting scan of log files ---")
    ret["log"].append(f"INFO: number of files to process: {ret['checked_num']}")

    # match names of tables in resource files to names of metadata in files

    metadata_categorical_in_files = [
        "building_category",
        "cooling_source",
        "energy_eff_standard",
        "dhw_heat_source",
        "sh_heat_source",
        "ventilation_heat_source",
        "snow_melt_heat_source",
        "ventilation_types",
    ]

    metadata_categorical_in_resource_files = [
        "building_categories",
        "cooling_sources",
        "energy_eff_standards",
        "heat_sources",
        "heat_sources",
        "heat_sources",
        "heat_sources",
        "ventilation_types",
    ]

    metadata_categorical = list(zip(metadata_categorical_in_files, metadata_categorical_in_resource_files))

    # start progress bar
    progress_bar = Bar(
        "Checking log files",
        max=len(files_to_check),
        suffix="[%(index)d/%(max)d] - [%(eta_td)s - %(elapsed_td)s]",
    )

    for file in files_to_check:
        ret["log"].append(f"INFO: --- processing file: {file}")

        # read metadata from each file
        metadata_in_file = treaData.getTreaCsvMetaData(file)

        # check for building_id
        if "building_id" in metadata_in_file:
            ret["log"].append(f"INFO: file contains 'building_id' value '{metadata_in_file['building_id']}'")

        # check for data_source
        if "data_source" in metadata_in_file:
            ret["log"].append(f"INFO: file contains 'data_source' value '{metadata_in_file['data_source']}'")
        else:
            ret["log"].append(f"ERROR: {file}: metadata 'data_source' not found in file")
            ret["errors_num"] += 1
            if file not in ret["errors_files"]:
                ret["errors_files"].append(file)

        # verify values in categorical metadata

        # verify building_category, extra check since it is a required field
        if "building_category" not in metadata_in_file:
            ret["log"].append(f"ERROR: {file}: required metadata 'building_category' not found")
            ret["errors_num"] += 1
            if file not in ret["errors_files"]:
                ret["errors_files"].append(file)

        # loop through other categorical metadata
        for metadata_categorical_in_file, metadata_categorical_in_resource_file in metadata_categorical:
            if metadata_categorical_in_file in metadata_in_file:

                value = metadata_in_file[metadata_categorical_in_file]

                ret["log"].append(
                    f"INFO: found categorical metadata '{metadata_categorical_in_file}', value '{value}'"
                )

                # split value into list, try various formats

                if " " not in value and "," not in value:
                    # likely single value
                    metadata_list = [
                        value,
                    ]
                elif " " in value and "," in value:
                    # likely format "XX, XX, XX"
                    metadata_list = value.replace(" ", "")
                    metadata_list = metadata_list.split(",")
                elif " " not in value and "," in value:
                    # likely format "XX,XX,XX"
                    metadata_list = value.split(",")
                # elif " " in value and "," not in value:
                #     # likely format "XX XX XX"
                #     metadata_list = value.split(" ")
                else:
                    ret["log"].append(
                        f"ERROR: {file}: unable to parse metadata: metadata '{metadata_categorical_in_file}', value '{metadata_in_file[metadata_categorical_in_file]}'"
                    )
                    ret["errors_num"] += 1
                    if file not in ret["errors_files"]:
                        ret["errors_files"].append(file)

                for item in metadata_list:
                    if item in accepted_unknowns and not item == "Ukn":
                        ret["log"].append(f"INFO: value '{item}' replaced with 'Ukn'")
                        item = "Ukn"

                    if item in metadata[metadata_categorical_in_resource_file]:
                        ret["log"].append(f"INFO: value '{item}' found in allowed list")
                    else:
                        ret["log"].append(
                            f"ERROR: {file}: metadata '{metadata_categorical_in_file}' value '{item}' not found in allowed list"
                        )
                        ret["errors_num"] += 1
                        if file not in ret["errors_files"]:
                            ret["errors_files"].append(file)

        # check that numeric metadata is numeric

        metadata_integer_values_list = [
            "year_of_construction",
            "floor_area",
            "heated_floor_area",
            "number_of_users",
            "number_of_units",
            "number_of_buildings",
            "central_heating_system",
            "night_setback",
            "lighting_control",
            "influenced"
        ]

        for key in metadata_in_file:
            # if metadata_in_file[key] == "":
            #     ret["log"].append(f"WARN: {file}: {key} is empty, value '{metadata_in_file[key]}'")

            if key in metadata_integer_values_list and metadata_in_file[key] != "":
                if metadata_in_file[key].replace(".", "").isnumeric():
                    ret["log"].append(f"INFO: numeric metadata {key} appears numeric, value '{metadata_in_file[key]}'")
                elif metadata_in_file[key] in accepted_unknowns:
                    ret["log"].append(f"INFO: numeric metadata {key} appears unknown, value '{metadata_in_file[key]}'")
                else:
                    ret["log"].append(
                        f"ERROR: {file}: numeric metadata '{key}' appears non-numeric, value '{metadata_in_file[key]}'"
                    )
                    ret["errors_num"] += 1
                    if file not in ret["errors_files"]:
                        ret["errors_files"].append(file)

        # verify date, not bulletproof, but will catch some errors
        # invalid datetime like "2022-01-01 13:5" will be allowed (lacking zero padding on minute)

        if "last_update" in metadata_in_file:
            try:
                datetime.datetime.fromisoformat(metadata_in_file["last_update"])
                ret["log"].append(f"INFO: 'last_update' date format appears valid: {metadata_in_file['last_update']}")
            except ValueError:
                ret["log"].append(
                    f"ERROR: {file}: incorrect date format, 'last_update': {metadata_in_file['last_update']}, should be 'YYYY-MM-DD' or 'YYYY-MM-DD hh:mm'"
                )
                ret["errors_num"] += 1
                if file not in ret["errors_files"]:
                    ret["errors_files"].append(file)

        # update progress bar
        progress_bar.next()

    # end progress bar
    progress_bar.finish()

    # build return values
    for line in ret["log"]:
        if line[:4] == "WARN":
            ret["warnings"].append(line)
        elif line[:5] == "ERROR":
            ret["errors"].append(line)

    # change directory back to original working directory
    os.chdir(original_directory)

    return ret


def write_log_to_file(log: list[str], filename: str, error: str = None, warn: str = None):
    """
    Write return values from check_logfiles() to files.

    If error or warn are provided, use them as filenames to write the error and/or warning log.
    """

    # write entire log to filename
    if log is not None and filename is not None:
        with open(filename, "w") as outfile:
            for line in log["log"]:
                outfile.write(f"{line}\n")
    else:
        print("ERROR: could not write log, log and filename must be provided")
        return

    # if error is passed, write errors to error
    if error is not None:
        with open(error, "w") as outfile:
            if not log["errors"]:
                outfile.write("No errors.")
            else:
                for line in log["errors"]:
                    outfile.write(f"{line}\n")

    # if warn is passed, write warnings to warn
    if warn is not None:
        with open(warn, "w") as outfile:
            if not log["warnings"]:
                outfile.write("No warnings.")
            else:
                for line in log["warnings"]:
                    outfile.write(f"{line}\n")


def import_data(files: list[str] = None, directory: str = None, filetype: str = ".txt"):
    """
    Import files previously checked with check_logfiles().

    Main stages:
    1. Read file metadata, create building in table "buildings" if it does not exist
    2. Read file timeseries data, insert into table "timeseries", linked to entry in "buildings"
    3. Write info to .csv in same directory linking filename and building_id
    """

    # abort if no files or directory are supplied
    if files is None and directory is None:
        print("Error: no files or directory in function call, aborting")
        return

    # if directory is provided, ignore files argument and instead scan directory for files
    if directory is not None:
        original_directory = os.getcwd()
        os.chdir(directory)
        files = os.listdir()

    # filter files by filetype
    files_to_import = []
    for file in files:
        if file[-4:] == filetype:
            files_to_import.append(file)

    files = files_to_import

    # pprint(f"Files to import: {files}")

    # -----
    # Stage 1: Read file metadata, create building in table "buildings" if it does not exist

    # read full set of metadata from resource file
    # calling os.path.dirname twice to go to parent directory of __file__
    metadata_list = list(
        pd.read_csv(f"{os.path.dirname(os.path.dirname(__file__))}\\resources\\metadata.csv", sep=";")[
            "description_short"
        ]
    )

    # remove building_id from metadata list
    metadata_list.remove("building_id")

    # pprint(metadata_list)
    # sys.exit()

    # check if folder for imported files exist, and create if not
    if not os.path.exists("imported"):
        print("folder for imported files does not exist, creating")
        os.makedirs("imported")
        

    for file in files:
        # ready dictionary with all fields from metadata.csv, populating with default values
        metadata = {}

        metadata_integer_values_list = [
            "year_of_construction",
            "floor_area",
            "heated_floor_area",
            "number_of_users",
            "number_of_units",
            "number_of_buildings",
            "central_heating_system",
            "night_setback",
            "lighting_control",
            "influenced",
        ]

        # set integer values to default 0
        for key in metadata:
            if key in metadata_integer_values_list:
                metadata[key] = None

        # specific default unknown values for some metadata
        metadata["night_setback"] = 2
        metadata["lighting_control"] = 2
        metadata["central_heating_system"] = 2

        metadata_file = treaData.getTreaCsvMetaData(file)

        # insert metadata from file into metadata dictionary, lowercase keys
        for key in metadata_file:
            metadata[key.lower()] = metadata_file[key]

        print(f"=== importing {file} ===")

        # if metadata contains building_id, only insert new timeseries linked to building_id
        # else, create new building
        if "building_id" in metadata:
            building_id = metadata["building_id"]
            print(
                f"INFO: file contains building_id, value = {building_id}. Not creating new building, only inserting time series."
            )
        else:
            print("INFO: building_id not found, creating new building.")

            # remove Header_line
            metadata.pop("header_line", None)

            # sanitize data

            for key in metadata:
                # make sure everything is string
                metadata[key] = str(metadata[key])

                # trim whitespace off strings
                if metadata[key] in metadata_categorical_lists:
                    metadata[key] = ",".join([x.strip() for x in metadata[key].split(',')])
                metadata[key] = metadata[key].strip()

                # replace some common zero/unknown values with None
                if metadata[key] in accepted_unknowns:
                    metadata[key] = None

                # convert strings to intergers for integer values
                if (key in metadata_integer_values_list and
                        metadata[key] is not None):
                    # numeric-looking strings to int (like "25.0")
                    if metadata[key].replace(".", "").isnumeric():
                        metadata[key] = int(float(metadata[key]))
                    else:
                        try:
                            metadata[key] = int(metadata[key])
                        except ValueError:
                            print(
                                f"ERROR: {file}: metadata key {key} not numeric, value '{metadata[key]}'. Aborting import."
                            )
                            sys.exit()


                # # float to int
                # if isinstance(metadata[key], float):
                #     metadata[key] = int(metadata[key])

                # make sure location is text
                # some logs contain only a postcode and thus appear as int
                # if key == "location":
                #     metadata[key] = str(metadata[key])

                # make sure values in metadata_integer_values_list are still int
                # if key in metadata_integer_values_list:
                #     if metadata[key] in accepted_unknowns:
                #         metadata[key] = None
                #     else:
                #         try:
                #             _ = int(metadata[key])
                #         except ValueError:
                #             print(
                #                 f"ERROR: {file}: metadata key {key} not numeric, value '{metadata[key]}'. Aborting import."
                #             )
                #             sys.exit()

                # if last_update is not a valid date, set to year 1900
                if key == "last_update" and metadata[key] is not None:
                    try:
                        datetime.datetime.fromisoformat(metadata[key])
                    except ValueError:
                        print(
                            f"WARN: {file}: {key} not a valid date with time zone, value '{metadata[key]}'. Setting to year 1900."
                        )
                        metadata[key] = "1900-01-01"

            # strip None values
            metadata = {key: value for key, value in metadata.items() if value is not None}

            # insert into buildings table
            data = pd.DataFrame([metadata])

            # returns True if data was inserted (ie building was new), False if building already existed
            new_building = db_insert("buildings", data)

            if new_building:
                # look up the id of the building we just created
                with psycopg.connect(cred) as conn:
                    building_id = conn.execute("select max(id) from buildings").fetchall()[0][0]

                # write building_id and filename to import.log
                # check if header should be added (if file does not exist or has no data)
                add_header = True
                try:
                    if os.path.getsize("import.log"):
                        add_header = False
                except:  # file does not exist
                    pass
                with open("import.log", "a", newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=";")
                    if add_header:
                        writer.writerow(["building_id", "source_file", "data_source"])
                    writer.writerow([building_id] + [f"{directory}\\{file}"] + [metadata["data_source"]])
            else:
                print(f"ERROR: {file}: Error inserting into database, aborting.")
                sys.exit()

        # ---
        # Stage 2. Read file timeseries data, insert into table "timeseries", linked to entry in "buildings"

        # set metadata back to full version of metadata, since we modified it above for convenience
        # metadata = metadata_full.copy()

        # read time series data
        timeseries = treaData.getTreaCsvTimeSeries(file, metadata_file)

        # build dictionary of data to be imported
        import_data = {}
        import_data["building"] = building_id

        # add space separated string of available timeseries data types
        import_data["measurement_types"] = " ".join(timeseries.columns)

        # reset index for easy import to database
        timeseries.reset_index(inplace=True)

        # add smallest and biggest timestamp
        import_data["timestamp_from"] = min(timeseries["TimeStamp"])
        import_data["timestamp_to"] = max(timeseries["TimeStamp"])

        # resolution, taking time difference between two first entries in log, reporting in seconds
        import_data["resolution"] = (timeseries["TimeStamp"][1] - timeseries["TimeStamp"][0]).seconds

        # write temporary .csv to disk, read .csv back in as binary without decoding, delete temporary file
        # random temporary file name
        # temp_file = "q5XjqcNegYGX1m.csv"

        timeseries_csv = timeseries.to_csv(index=False)

        # read file back in as binary
        # with open(temp_file, "rb") as csv_file:
        #     mydata = csv_file.read()
        # os.remove(temp_file)

        import_data["data"] = timeseries_csv

        # convert to DataFrame, adding dummy index
        import_data = pd.DataFrame(import_data, index=[0])

        # insert DataFrame into database
        db_insert("timeseries", import_data)

        # move imported file to imported folder
        os.rename(file, f"imported/{file}")
        
        # print("Timeseries written to database.")
        print(f"--- done importing {file} ---")

    # change directory back to original working directory
    if directory:
        os.chdir(original_directory)


def create_clause(metadata):
    """
    Create clause for database query based on metadata dictionary
    Returns a sql WHERE clause string
    """

    # build WHERE clause string from columns
    # format: "column = %s AND column = %s" for items, "BETWEEN %s AND %s" for ranges
    clause = []
    for key, value in metadata.items():

        # integer input, simple case
        if type(value) == int:
            clause.append(key + f" = {value}")

        # string inputs
        if type(value) == str:
            if "-" in value:
                # assume an integer range, e.g. 2012-2014, including all years between
                value_from, value_to = value.split("-")
                clause.append(key + f" BETWEEN {value_from} AND {value_to}")
            elif "+" in value:
                # assume all listed values are required
                values = value.split("+")
                values = ",".join(["'" + x.strip() + "'" for x in values])
                clause.append(f"string_to_array({key}, ',') @> array[{values}]")
            elif "," in value:
                # assume one or more of listed values is required
                values = value.split(",")
                values = ",".join(["'" + x.strip() + "'" for x in values])
                clause.append(f"string_to_array({key}, ',') && array[{values}]")
            else:
                # single string value
                clause.append(key + f" = '{value}'")

    if len(clause) == 0:
        clause = None
    else:
        clause = " AND ".join(clause)
    return clause


def export_buildings(building_ids, directory=None):
    """
    Export data from database based on list of building ids

    Returns a dictionary of building data sorted by building id.
    If directory is supplied, writes out .csv files by building id.

    """
    # dictionary to store results in
    buildings = {}

    # start progress bar
    progress_bar = Bar("Exporting files", max=len(building_ids))

    for building_id in building_ids:
        metadata = db_select("buildings", clause=f"id = {building_id['id']}")

        timeseries = db_select("timeseries", column="data", clause=f"building = {building_id['id']}")

        # write binary stored .csv timeseries to file to read back in as pandas .csv

        # random temporary file name
        temp_file = "q5XjqcNegYGX1m.csv"

        with open(temp_file, "wb") as csv_file:
            csv_file.write(timeseries[0]["data"])

        # using pandas read_csv to maintain compatibility
        timeseries_decoded = pd.read_csv(temp_file)
        os.remove(temp_file)

        # setting index on TimeStamp column
        timeseries_decoded = timeseries_decoded.set_index("TimeStamp")

        # break out from list
        metadata = metadata[0]

        # add header_line info
        metadata = treaData.addHeaderLine(metadata)

        # rename id to building_id in metadata
        metadata["building_id"] = metadata.pop("id")

        if directory:
            treaData.writeTreaCsv(directory, f"export_{building_id['id']}", metadata, timeseries_decoded)

        # add building to result dictionary
        buildings[building_id["id"]] = (metadata, timeseries_decoded)

        # update progress bar
        progress_bar.next()

    # end progress bar
    progress_bar.finish()

    return buildings


def export_data(metadata, directory=None, overwrite=False, force_export=False):
    """
    Export data from database.

    Returns a dictionary of building data sorted by building id.
    If directory is supplied, writes out .csv files by building id.

    Main stages:
    1. Find matching building ids in "buildings" table

    For all buildings found:
    2. Look up building by id in "buildings" table
    3. Look up all timeseries for that building from "timeseries" table
    4. Write to file

    """

    # ---
    # Stage 1: Find matching building ids in "buildings" table
    clause = create_clause(metadata)

    # look up building ids matching clause
    building_ids = db_select("buildings", column="id", clause=clause)

    if not overwrite:
        if not directory:
            print("Warning: overwrite not valid option when data is not stored")
        # remove buildings already in directory
        elif not os.path.exists(directory):
            print("Directory does not exist, creating.")
        else:
            # get ids in folder:
            files = os.listdir(directory)
            existing_ids = []
            for f in files:
                try:
                    existing_ids.append(int(f.split("_")[1][:-4]))
                except:
                    continue
            building_ids = [x for x in building_ids if list(x.values())[0] not in existing_ids]

    if len(building_ids) == 0:
        print("No new matching buildings found")
        return {}

    if not force_export:
        # ask if user want to proceed
        if not b_utils.query_yes_no(f"{len(building_ids)} matches found, continue to export?"):
            return building_ids

    # ---
    # 2. Look up building by id in "buildings" table in database

    buildings = export_buildings(building_ids, directory=directory)

    return buildings


def db_get_id(table: str, column: str, property: str):
    """Gets a single id. Useful to find ids in categorical tables.
    Returns id as an integer."""

    # print(f"Looking up the id of '{property}' in table {table}, in the '{column}' column.")

    # conn.execute expects an iterable containing the string, not the string itself. Using tuple.
    property = (property,)

    with psycopg.connect(cred) as conn:
        id = conn.execute(f"SELECT id FROM {table} WHERE {column} = %s", property).fetchall()[0][0]

    return id


def db_get_metadata(table, column=None):
    """
    Helper function to retrieve various metadata from database.

    Recommended for use on the following tables in database:

    building_categories, cooling_sources, data_sources, energy_eff_standards,
    heat_sources, measurement_types, pv_locations, units, ventilation_types

    If no column parameter is given, return a dictionary with all data in the table.
    If a column parameter is given, return the contents of the column as a list.
    """

    if column is None:
        # print(f"Retrieving all entries in table '{table}'.")

        # using row_factory=dict_row to get data back as a dictionary
        with psycopg.connect(cred, row_factory=dict_row) as conn:
            data = conn.execute(f"SELECT * FROM {table}").fetchall()

        return data
    else:
        # print(f"Retrieving column '{column}' from table '{table}'.")

        with psycopg.connect(cred) as conn:
            data = conn.execute(f"SELECT {column} FROM {table}").fetchall()

        items = [item for tup in data for item in tup]
        return items


def db_insert(table: str, data: pd.DataFrame):
    """
    Inserts into database using COPY. A lot faster than INSERT on many entries.

    Expects a pandas dataframe with named columns matching database table column
    names as input.

    Checks for duplicates, stop and return False if the data is already found in the database.
    Returns True if data was inserted.

    """

    # print(f"INFO: Attempting to insert {len(data)} rows in table '{table}', columns: {', '.join(data.columns)}.")

    # fill NaNs in DataFrame with empty string to match empty fields in postgreSQL tables
    data.fillna("", inplace=True)

    # connect to database
    with psycopg.connect(cred) as conn:
        cur = conn.cursor()

        # check if any of the lines already exist in database
        existing_rows = 0

        # print("INFO: Starting check for duplicate rows.")

        # build string from columns with format "column = %s AND column = %s AND column %s"
        query_condition = []
        for column in data.columns:
            query_condition.append(f"{table}.{str(column) + ' = %s'}")
        query_condition = " AND ".join(query_condition)

        query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {query_condition})"

        for row in data.itertuples(index=False):
            exists = conn.execute(query, row).fetchall()
            if exists[0][0] is True:
                existing_rows += 1

        # if rows exist, abort
        if existing_rows > 0:
            print(f"ERROR: Existing duplicate rows found: {existing_rows}. Aborting. No rows inserted.")
            return False
        else:
            # print("INFO: No duplicate rows found, continuing.")

            # building string of columns with format "column, column, column"
            query_columns = ", ".join(data.columns)

            # insert all rows
            with cur.copy(f"COPY {table} ({query_columns}) FROM STDIN") as copy:
                for row in data.itertuples(index=False):
                    copy.write_row(row)

            # print(f"INFO: Done inserting. Inserted {len(data)} row(s) in table {table}.")
            return True


def db_insert_metadata(table: str, file: str):
    """
    Helper function to insert data from .csv files in /resources/ into database.

    Function ends up very simple, but bases its simplicity on three things:
    * pandas DataFrames are directly iterable by psycopg and may be passed as data
    * the .csv files in /resources are formatted properly
    * fields (columns) matching the .csv already exist in the database.

    Required format of .csv files:
    field;field;field
    data;data;data
    data;data;data

    Example usage:
    db_insert_metadata("energy_eff_standards", "gitlab/Buildings/resources/energy_eff_standards.csv")
    """

    data = pd.read_csv(file, sep=";")
    db_insert(table, data)


def db_select(table, column=None, clause=None):
    """
    Helper function to retrieve data from database.

    If no column parameter is given, return a dictionary with all data in the table.
    If a column parameter is given, return the contents of the column as a list.
    If a clause is given, filter on the clause.
    """

    if column is None:
        query_column = "*"
    else:
        query_column = column

    if clause is None:
        query_clause = ""
    else:
        query_clause = f"WHERE {clause}"

    query = f"SELECT {query_column} from {table} {query_clause}"

    # debug
    # print(f"db_select: {query}")

    # using row_factory=dict_row to get data back as a dictionary
    with psycopg.connect(cred, row_factory=dict_row) as conn:
        data = conn.execute(query).fetchall()

    return data


def db_wipe_table(table):
    """

    Helper function to delete all entries in a table. Use with caution.

    Example usage:
    db_wipe_table("buildings")
    """

    print(f"Deleting all entries in table '{table}'.")

    with psycopg.connect(cred) as conn:
        conn.execute(f"DELETE FROM {table}")
