import json

peakdata=''

def loadDatabaseFile():
    with open('peak_data.json','r') as read_file:
        print('decoding file')
        peakdata = json.load(read_file)
    return peakdata


