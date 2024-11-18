import math
import time
from EVA import globals
from EVA.app import get_app
from EVA.globals import muon_database, peak_data


def getmatchesgammastrans_clicked(Ele, En):
    app = get_app()
    print('length of full_gamms', len(app.gamma_database))
    print('Ele', Ele)
    print('En', En)
    all_matches = []
    i = 1
    while i < len(app.gamma_database)-1:
        i += 1
        for j in range(len(app.gamma_database[i])):
            raw_data = app.gamma_database[i][j]

            delme = 0

            if Ele == raw_data[0].strip():

                '''print('raw_data', raw_data[0])
                print(str(Ele).strip(), raw_data[0].strip(), En, float(raw_data[1])*1000.0,
                      raw_data[2],raw_data[3], len(globals.Full_Gammas[i]))
                print('list', globals.Full_Gammas[i][j])'''
                raw_data_kev = float(raw_data[1]) * 1000.0
                sigma = 0.005 * raw_data_kev

                if float(En) > raw_data_kev - sigma and float(En) < raw_data_kev + sigma:
                    print('En matched')
                    data = {}

                    data['Element'] = raw_data[0]
                    data['Energy'] = raw_data_kev
                    data['Intensity'] = raw_data[2]
                    data['lifetime'] = raw_data[3]
                    all_matches.append(data)
                #print('hello',delme)
                delme += 1

    #print('all_matches', all_matches)

    return all_matches

def getmatchesgammastrans_clicked_old(Ele, En):
    print('length of full_gamms', len(globals.Full_Gammas))
    print('Ele', Ele)
    print('En', En)
    all_matches = []
    i = 1
    while i < len(globals.Full_Gammas)-1:
        i += 1
        for j in range(len(globals.Full_Gammas[i])):
            raw_data = globals.Full_Gammas[i][j]

            delme = 0

            if Ele == raw_data[0].strip():

                '''print('raw_data', raw_data[0])
                print(str(Ele).strip(), raw_data[0].strip(), En, float(raw_data[1])*1000.0,
                      raw_data[2],raw_data[3], len(globals.Full_Gammas[i]))
                print('list', globals.Full_Gammas[i][j])'''
                raw_data_kev = float(raw_data[1]) * 1000.0
                sigma = 0.005 * raw_data_kev

                if float(En) > raw_data_kev - sigma and float(En) < raw_data_kev + sigma:
                    print('En matched')
                    data = {}

                    data['Element'] = raw_data[0]
                    data['Energy'] = raw_data_kev
                    data['Intensity'] = raw_data[2]
                    data['lifetime'] = raw_data[3]
                    all_matches.append(data)
                #print('hello',delme)
                delme += 1

    #print('all_matches', all_matches)

    return all_matches


def getmatchesgammas_clicked(Ele):
    app = get_app()
    all_matches = []
    i = 1
    while i < len(app.gamma_database)-1:
        i += 1
        #print('i=',i)
        for j in range(len(app.gamma_database[i])):

            raw_data = app.gamma_database[i][j]

            if str(Ele) == raw_data[0].strip():
                data = {}
                raw_data_kev=float(raw_data[1])*1000

                data['Element'] = raw_data[0]
                data['Energy'] = raw_data_kev
                data['Intensity'] = raw_data[2]
                data['lifetime'] = raw_data[3]

                all_matches.append(data)

    return all_matches


def getmatchesgammas_clicked_old(Ele):
    print('length of full_gamms', len(globals.Full_Gammas))
    print('Ele', Ele)
    all_matches = []
    i = 1
    while i < len(globals.Full_Gammas)-1:
        i += 1
        #print('i=',i)
        for j in range(len(globals.Full_Gammas[i])):

            raw_data = globals.Full_Gammas[i][j]
            #print(Ele,raw_data[0])
            if str(Ele) == raw_data[0].strip():
                data = {}
                raw_data_kev=float(raw_data[1])*1000

                data['Element'] = raw_data[0]
                data['Energy'] = raw_data_kev
                data['Intensity'] = raw_data[2]
                data['lifetime'] = raw_data[3]
                #print(data)
                all_matches.append(data)
    #print('all_matches', all_matches)

    return all_matches


def get_matches_Element_PrimorSec(input_element, PrimorSec):
    print(input_element)
    matches = []
    Primary_matches = []
    Secondary_matches = []


    for x in globals.peak_data:

        print('x',x)
        raw_data = globals.peak_data[x]
        for element in raw_data:
            if element == input_element:
                for transition, energy in raw_data[element].items():
                    data = {}
                    data['element'] = element
                    data['energy'] = energy
                    data['transition'] = transition
                    matches.append(data)
        if x == 'Primary energy':
            print('PrimE')
            Primary_matches = matches
            matches = []
        if x == 'Secondary energy':
            print('SecE')
            Secondary_matches = matches
            matches = []
    if PrimorSec == 'Primary':
        print('Primmatch')
        rtn_matches = Primary_matches
    elif PrimorSec == 'Secondary':
        print('Secmatch')
        rtn_matches = Secondary_matches

    #print(rtn_matches)

    return rtn_matches

def get_matches_Trans(input_element, input_trans):
    app = get_app()
    raw_data = app.muon_database

    matches = []
    raw_data = app.muon_database["All energies"]

    for element in raw_data:
        if element == input_element:
            for transition, energy in raw_data[element].items():
                if transition == input_trans:
                    data = {
                        "element": element,
                        "energy": energy,
                        "transition": transition
                    }
                    matches.append(data)

    return matches

def get_matches_Trans_old(input_element, input_trans):
    matches = []
    for x in globals.peak_data:
        raw_data = globals.peak_data[x]
        for element in raw_data:
            if element == input_element:
                for transition, energy in raw_data[element].items():
                    if transition == input_trans:
                        data = {}
                        data['element'] = element
                        data['energy'] = energy
                        data['transition'] = transition
                        matches.append(data)


    return matches

def get_matches_Element(input_element):
    app = get_app()
    matches = []

    raw_data = app.muon_database["All energies"]
    for element in raw_data:
        if element == input_element:
            for transition, energy in raw_data[element].items():
                data = {
                    "element": element,
                    "energy": energy,
                    "transition": transition
                }
                matches.append(data)

    return matches

def get_matches_Element_old(input_element):

    matches = []
    for x in globals.peak_data:
        raw_data = globals.peak_data[x]
        for element in raw_data:
            if element == input_element:
                for transition, energy in raw_data[element].items():
                    data = {}
                    data['element'] = element
                    data['energy'] = energy
                    data['transition'] = transition
                    matches.append(data)

    #print(matches)

    return matches

# new, faster version
def get_matches(input_peaks):
    start_time = time.time_ns()
    app = get_app()
    peak_data = app.muon_database

    primary_matches = []
    secondary_matches = []
    all_matches = []
    prims = []

    raw_data = peak_data["All energies"]
    for peak, sigma in input_peaks:
        for element in raw_data:
            for transition, energy in raw_data[element].items():
                diff = abs(peak - energy)

                if diff <= 3*sigma:
                    data = {
                        "element": element,
                        "energy": energy,
                        "error": math.ceil(diff/sigma) * sigma,
                        "peak_centre": peak,
                        "transition": transition,
                        "diff": diff
                    }

                    all_matches.append(data)

            prims = [peak[0] for peak in peak_data["Primary energies"][element].items()]

    all_matches = sorted(all_matches, key=lambda o: o['diff'])

    for match in all_matches:
        if match["transition"] in prims:
            primary_matches.append(match)
        else:
            secondary_matches.append(match)

    end_time = time.time_ns()
    print(f"Found matches in {(end_time - start_time) / 1e9} s.")

    return all_matches, primary_matches, secondary_matches

# previous, slower version
def get_matches_slow(input_peaks):
    app = get_app()
    peak_data = app.muon_database

    all_matches = []
    Primary_matches = []
    Secondary_matches = []
    for x in peak_data:
        #print('x=' + x)
        raw_data = peak_data[x]
        #print('raw_data at x', raw_data)
        matches = []
        for peak, sigma in input_peaks:
            for element in raw_data:
                for transition, energy in raw_data[element].items():
                    if peak == energy:
                        data = {}
                        data['element'] = element
                        data['energy'] = energy
                        data['error'] = 0
                        data['peak_centre'] = peak
                        data['transition'] = transition
                        data['diff'] = 0
                        matches.append(data)

                    elif peak >= (energy - sigma) and peak <= (energy + sigma):
                        data = {}
                        data['element'] = element
                        data['energy'] = energy
                        data['error'] = sigma
                        data['peak_centre'] = peak
                        data['transition'] = transition
                        data['diff'] = abs(peak - energy)
                        matches.append(data)

                    elif peak >= (energy - 2 * sigma) and peak <= (energy + 2 * sigma):
                        data = {}
                        data['element'] = element
                        data['energy'] = energy
                        data['error'] = 2 * sigma
                        data['peak_centre'] = peak
                        data['transition'] = transition
                        data['diff'] = abs(peak - energy)
                        matches.append(data)

                    elif peak >= (energy - 3 * sigma) and peak <= (energy + 3 * sigma):
                        data = {}
                        data['element'] = element
                        data['energy'] = energy
                        data['error'] = 3 * sigma
                        data['peak_centre'] = peak
                        data['transition'] = transition
                        data['diff'] = abs(peak - energy)
                        matches.append(data)

        matches = sorted(matches, key=lambda o: o['diff'])
        #print(matches)
        if x == 'Primary energy':
            Primary_matches = matches
        if x == 'Secondary energy':
            Secondary_matches = matches

    all_matches.append(matches)

    return all_matches, Primary_matches, Secondary_matches

def getmatchesgammas(input_peaks):
    app = get_app()
    print('length of full_gamms', len(app.gamma_database))
    all_matches = []
    i = 1
    while i < len(app.gamma_database)-1:
        i += 1
        #print('i=',i)
        for j in range(len(app.gamma_database[i])):

            raw_data = app.gamma_database[i][j]
            #print('raw_data', raw_data)
            for peak, sigma in input_peaks:
                raw_data_kev=float(raw_data[1])*1000

                if peak >= (raw_data_kev - sigma) and peak <= (raw_data_kev + sigma):
                 #print('in print', peak, sigma, raw_data)
                    data = {}
                    data['Element'] = raw_data[0]
                    data['Energy'] = raw_data_kev
                    data['diff'] = peak - float(raw_data_kev)
                    #print(data['diff'])
                    data['Intensity'] = raw_data[2]
                    data['lifetime'] = raw_data[3]
                    all_matches.append(data)

    all_matches.sort(key = lambda x: abs(x['diff']))

    return all_matches
