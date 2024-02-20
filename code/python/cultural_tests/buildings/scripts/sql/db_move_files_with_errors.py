import buildings.lib.treaSQL as treaSQL
import os
import shutil

# --------------------------------------------------------------------------------
# move files with errors to subdirectory

# directory = "import_files_2_0"
# directory = "import_statnett_treated_data"

user='hwaln@sintef.no' #change to your username
treaSQL.cred=treaSQL.get_credentials(user)

directory = "import_Byggfiler120123"

mylog = treaSQL.check_logfiles(directory=directory)

# write log to file
treaSQL.write_log_to_file(mylog, filename=f"{directory}/00 log.log", error=f"{directory}/00 error.log")

# check_logfiles returns a dictionary of results, including a list of files with errors
files_with_errors = mylog["errors_files"]

# user defined directory
error_directory = "files_with_errors"

if len(files_with_errors) > 0:
    print(f"Errors found. Moving {len(files_with_errors)} files to subdirectory '{error_directory}'.")
    original_directory = os.getcwd()
    os.chdir(directory)

    if not os.path.exists(error_directory):
        os.makedirs(error_directory)

    for file in files_with_errors:
        shutil.move(file, f"{error_directory}\\{file}")

    os.chdir(original_directory)
else:
    print("No errors, not moving any files.")
