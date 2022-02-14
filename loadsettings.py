settings_info = ''
def loadsettings():
    with open('Settings.txt') as f:
        lines = f.readlines()
        print(lines)
        settings_info=lines

'''def loadsettings(filename):
    with open(filename) as f:
        lines = f.readlines()
        print(lines)
        settings_info=lines
'''

