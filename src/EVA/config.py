from configparser import ConfigParser
parser = ConfigParser()
def init():
    parser.read("./src/EVA/config.ini")
def restore_defaults():
    default_parser = ConfigParser()
    default_parser.read("./src/EVA/defaults.ini")
    for section in default_parser:
        parser[section] = default_parser[section]

def save_config():
    with open("./src/EVA/config.ini", "w") as config_file:
        parser.write(config_file)
        config_file.close()
