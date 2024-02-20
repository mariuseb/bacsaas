import buildings.lib.treaSQL as treaSQL
from pprint import pprint

# --------------------------------------------------------------------------------
# import example

# ---
# specify a directory containing logs

# directory = "import_files_2_0"
# directory = "import_statnett_treated_data"

user='hwaln@sintef.no' #change to your username
treaSQL.cred=treaSQL.get_credentials(user)

directory = "import_Byggfiler120123"

# ---
# run check_logfiles to verify no errors

# check_logfiles returns a dictionary of information
mylog = treaSQL.check_logfiles(directory=directory)

# inspect structure of returned dictionary
pprint(mylog, depth=1)

# extract some values
print(f"Errors found: {mylog['errors_num']}")
print(f"Files with errors: {mylog['errors_files']}")

# ---
# write logs to file

# write all three logs: the full log, the error log and the warnings log
treaSQL.write_log_to_file(
    mylog, filename=f"{directory}/00 log.log", error=f"{directory}/00 error.log", warn=f"{directory}/00 warn.log"
)

# only write the full log and error log
# treaSQL.write_log_to_file(mylog, filename=f"{directory}/00 log.log", error=f"{directory}/00 error.log")

# ---
# optional user input

# user_input = input("-- continue? [Y/n]: ")
# if user_input not in ["Y", "y", ""]:  # enter = empty string
#     print("Quitting.")
#     quit()

# ---
# if log returns no errors, do import

# treaSQL.import_data(directory=directory)
