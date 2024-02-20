import buildings.lib.treaSQL as treaSQL
from pprint import pprint
import json

# --------------------------------------------------------------------------------
# export example

def read_json_filter(filename):
    f = open(filename)
    fil = json.load(f)
    f.close()
    return fil

def dump_dict_to_json(metadata_filter, filename='filter.json'):
    with open(filename, "w") as outfile:
        json.dump(metadata_filter, outfile)
    return


user = "hwaln@sintef.no"  # change to your username
treaSQL.cred = treaSQL.get_credentials(user)

# metadata = {
#     "year_of_construction": "2012-2014",
#     "floor_area": "1000-2000",
#     "energy_eff_standard": "Eff",
#     "building_category": 'Apt'
# }

metadata = read_json_filter('filter.json')

# metadata = {"year_of_construction": "1943"}
# metadata = {"building_category": "Kdg, Schhkm, abc,def"}
# metadata = {"building_category": "Kdg,Sch"}
# metadata = {"building_category": "Apt"}

a = treaSQL.export_data(directory="./export/", metadata=metadata)
# a = treaSQL.export_data(metadata=metadata)

# pprint(type(a))
# print("Records found: " + str(len(a)))
# pprint(a, depth=1)
# pprint(a)
