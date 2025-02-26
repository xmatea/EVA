import json
from EVA.util.path_handler import get_path

# load iupac to spec notation conversion table
with open(get_path("src/EVA/databases/names/iupac_table_sorted.json"), "r") as file:
    IUPAC_TABLE = json.load(file)

# generate inverted table
SPEC_TABLE = {v: k for k, v in IUPAC_TABLE.items()}

def to_iupac(spec_name: str) -> str:
    """
    Args:
        spec_name: transition name in spectroscopic notation

    Returns:
        transition name in IUPAC notation
    """
    return IUPAC_TABLE[spec_name]


def to_spec(iupac_name: str) -> str:
    """
    Args:
        iupac_name: transition name in iupac notation

    Returns:
        transition name in spectroscopic notation
    """
    return SPEC_TABLE[iupac_name]

def is_primary(transition: str, notation:str = "spec") -> bool:
    """
    Args:
        transition: transition name
        notation: which notation is used for transition name (default is "spec", valid options are "spec, "iupac")

    Returns:
        Boolean indicating whether transition is primary or not.

    Checks if transition is primary or not by:

    * converting to IUPAC notation if not already

    * splitting transition name by "-", e.g. "K1-L2" -> ["K1", "L2"]

    * converting letter to integer using ord()

    * subtract the letters and check the difference - if difference is 1, letters are sequential and
    therefore transition is primary
    """
    if notation != "iupac":
        transition = to_iupac(transition) # this is easier to do on iupac notation

    e1, e2 = transition.split("-")  # split transition name
    return ord(e2[0]) - ord(e1[0]) == 1  # convert letter to integer and subtract
    # if letters are sequential their difference is 1
