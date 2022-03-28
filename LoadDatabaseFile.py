import json
import globals



def loadDatabaseFile():
    with open('./Databases/Muonic X-rays/peak_data.json','r') as read_file:
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




