import globals


def get_matches(input_peaks):
    all_matches = []
    for x in globals.peak_data:
        print('x=' + x)
        raw_data = globals.peak_data[x]
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

                    elif peak >= (energy - 3 * sigma) and peak <= (energy - 3 * sigma):
                        data['element'] = element
                        data['energy'] = energy
                        data['error'] = 3 * sigma
                        data['peak_centre'] = peak
                        data['transition'] = transition
                        data['diff'] = abs(peak - energy)
                        matches.append(data)
        matches = sorted(matches, key=lambda x: x['diff'])
        print(matches)
    all_matches.append(matches)
    print('kkk')
    print(all_matches)
    return all_matches
