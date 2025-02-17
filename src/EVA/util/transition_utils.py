import json
from EVA.util.path_handler import get_path

# load iupac to spec notation conversion table
with open(get_path("src/EVA/databases/names/iupac_table_sorted.json"), "r") as file:
    IUPAC_TABLE = json.load(file)

# generate inverted table
SPEC_TABLE = {v: k for k, v in IUPAC_TABLE.items()}


def to_iupac(spec_name):
    return IUPAC_TABLE[spec_name]


def to_spec(iupac_name):
    return SPEC_TABLE[iupac_name]

def is_primary(transition, notation ="spec"):
    if notation == "iupac":
        transition = to_iupac(transition) # this is easier to do on iupac notation

    e1, e2 = transition.split("-")  # split transition name, eg. "K1-L2" -> ["K1", "L2"]
    return ord(e2[0]) - ord(e1[0]) == 1  # convert letter to ASCII integer and subtract
    # if letters are sequential their difference is 1
