from configparser import ConfigParser
config_parser = ConfigParser()
def init():
    config_parser.read("./src/EVA/config.ini")
def restore_defaults():
    default_config_parser = ConfigParser()
    default_config_parser.read("./src/EVA/defaults.ini")
    for section in default_config_parser:
        config_parser[section] = default_config_parser[section]

def save_config():
    with open("./src/EVA/config.ini", "w") as config_file:
        config_parser.write(config_file)
        config_file.close()
