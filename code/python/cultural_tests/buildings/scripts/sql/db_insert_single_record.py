import pandas as pd
import buildings.lib.treaSQL as treaSQL

# --------------------------------------------------------------------------------
# inserting a single record

user='hwaln@sintef.no' #change to your username
treaSQL.cred=treaSQL.get_credentials(user)

data = pd.DataFrame(
    [{"name": "Ludvigsen AS", "contact": "Bjørn", "email": "bjorn.ludvigsen@sintef.no", "phone": "900 200 10"}]
)

# insert into data_sources table
treaSQL.db_insert("data_sources", data)
