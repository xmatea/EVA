settings_info = ''
def loadsettings():
    with open('src/EVA/Settings.txt') as f:
        lines = f.readlines()
        print(lines)
        settings_info=lines

'''def loadsettings(filename):
    with open(filename) as f:
        lines = f.readlines()
        print(lines)
        settings_info=lines
'''

