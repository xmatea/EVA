import json

def load_mudirac_data():
    with open('./src/EVA/databases/muonic_xrays/mudirac_data.json', 'r') as read_file:
        print('Loading mudirac database...')

        data = json.load(read_file)

        primary_energies_all_isotopes = {}
        secondary_energies_all_isotopes = {}
        all_energies_all_isotopes = {}

        primary_energies_default_isotope = {}
        secondary_energies_default_isotope = {}
        all_energies_default_isotope = {}

        # sort data
        for element in data:
            default_isotope = data[element]["Default"]

            for isotope in data[element]["Isotopes"]:
                primary_energy = {}
                secondary_energy = {}

                for p_trans in data[element]["Isotopes"][isotope]["Primary"]:
                    primary_energy[p_trans] = data[element]["Isotopes"][isotope]["Primary"][p_trans]["E"]

                for s_trans in data[element]["Isotopes"][isotope]["Secondary"]:
                    secondary_energy[s_trans] = data[element]["Isotopes"][isotope]["Secondary"][s_trans]["E"]

                primary_energies_all_isotopes[isotope] = primary_energy
                secondary_energies_all_isotopes[isotope] = secondary_energy
                all_energies_all_isotopes[isotope] = dict(primary_energy, **secondary_energy)

                if isotope == default_isotope:
                    primary_energies_default_isotope[element] = primary_energy
                    secondary_energies_default_isotope[element] = secondary_energy
                    all_energies_default_isotope[element] = dict(primary_energy, **secondary_energy)

        # Default to using only most abundant isotope
        peak_data = {
            "Primary energies": primary_energies_default_isotope,
            "Secondary energies": primary_energies_default_isotope,
            "All energies": all_energies_default_isotope,

            "All isotopes": {
                "Primary energies": primary_energies_all_isotopes,
                "Secondary energies": primary_energies_all_isotopes,
                "All energies": all_energies_all_isotopes
            }
        }

        return peak_data

def load_legacy_data():
    with open('./src/EVA/databases/muonic_xrays/peak_data.json', 'r') as read_file:
        print('Loading legacy database...')
        data = json.load(read_file)

        primary_energies = {}
        secondary_energies = {}
        all_energies = {}
        peak_data = {}

        # sort data
        for element in data:
            primary_energy = [float(x[1]) for x in list(data[element]['Primary'].items())]
            secondary_energy = [float(x[1]) for x in list(data[element]['Secondary'].items())]
            primary_trans = [x[0] for x in list(data[element]['Primary'].items())]
            secondary_trans = [x[0] for x in list(data[element]['Secondary'].items())]

            primary_energies[element] = dict(zip(primary_trans, primary_energy))
            secondary_energies[element] = dict(zip(secondary_trans, secondary_energy))
            all_energies[element] = dict(zip(primary_trans + secondary_trans,
                                             primary_energy + secondary_energy))
        peak_data['Primary energies'] = primary_energies
        peak_data['Secondary energies'] = secondary_energies
        peak_data['All energies'] = all_energies

        return peak_data

"""
def loadDatabaseFile():
    if globals.muon_database == "legacy":
        with open('./src/EVA/databases/muonic_xrays/peak_data.json', 'r') as read_file:
            print('decoding file')
            globals.peakdata = json.load(read_file)
            primary_energies = {}
            secondary_energies = {}
            all_energies = {}
            # sort data
            for element in globals.peakdata:
                primary_energy = [float(x[1]) for x in list(globals.peakdata[element]['Primary'].items())]
                secondary_energy = [float(x[1]) for x in list(globals.peakdata[element]['Secondary'].items())]
                primary_trans = [x[0] for x in list(globals.peakdata[element]['Primary'].items())]
                secondary_trans = [x[0] for x in list(globals.peakdata[element]['Secondary'].items())]

                primary_energies[element] = dict(zip(primary_trans, primary_energy))
                secondary_energies[element] = dict(zip(secondary_trans, secondary_energy))
                all_energies[element] = dict(zip(primary_trans + secondary_trans,
                                                 primary_energy + secondary_energy))
            globals.peak_data['Primary energy'] = primary_energies
            globals.peak_data['Secondary energy'] = secondary_energies
            globals.peak_data['All energies'] = all_energies

        return

    elif globals.muon_database == "mudirac":
        with open('./src/EVA/databases/muonic_xrays/mudirac_data.json', 'r') as read_file:
            print('decoding file')
            peakdata = json.load(read_file)
            primary_energies = {}
            secondary_energies = {}
            all_energies = {}

            # sort data
            for element in peakdata:
                for isotope in peakdata[element]["Isotopes"]:
                    primary_energy = {}
                    secondary_energy = {}
                    for p_trans in peakdata[element]["Isotopes"][isotope]["Primary"]:
                        primary_energy[p_trans] = peakdata[element]["Isotopes"][isotope]["Primary"][p_trans]["E"]

                    for s_trans in peakdata[element]["Isotopes"][isotope]["Secondary"]:
                        secondary_energy[s_trans] = peakdata[element]["Isotopes"][isotope]["Secondary"][s_trans]["E"]

                    primary_energies[isotope] = primary_energy
                    secondary_energies[isotope] = secondary_energy
                    all_energies[isotope] = dict(primary_energy, **secondary_energy)

            globals.peak_data['Primary energy'] = primary_energies
            globals.peak_data['Secondary energy'] = secondary_energies
            globals.peak_data['All energies'] = all_energies
"""