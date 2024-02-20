# database host, database name and credentials

host = "postgres.sintef.no"
dbname = "cofactor"
user = "bjornlu@sintef.no"

# building a libpq-formatted connection string
# naming it cs (for connection string) to keep it short

# references:
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
# https://www.psycopg.org/psycopg3/docs/api/conninfo.html
# https://www.psycopg.org/docs/module.html

cs = f"host={host} dbname={dbname} user={user}"
