import buildings.lib.treaSQL as treaSQL

# --------------------------------------------------------------------------------
# delete all data in database
# use with caution.

user = "hwaln@sintef.no"  # change to your username
treaSQL.cred = treaSQL.get_credentials(user)

treaSQL.db_wipe_table("buildings")
treaSQL.db_wipe_table("timeseries")
