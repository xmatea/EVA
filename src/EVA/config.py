from configparser import ConfigParser


class Config:
    """
    The config class uses the built-in module configparser to read and write configurations as .ini files.
    """
    def __init__(self):
        self.parser = ConfigParser()

    # This magic function allows the parser to be accessed when indexing directly into a config object:
    # Ex: it makes 'Config()["plot"]["fill_colour"]' equivalent to 'Config().parser["plot"]["fill_colour"]'
    def __getitem__(self, field: str):
        return self.parser[field]

    def load(self):
        self.parser.read("./src/EVA/config.ini")

    def save_config(self):
        with open("./src/EVA/config.ini", "w") as config_file:
            self.parser.write(config_file)
            config_file.close()

    def restore_defaults(self):
        default_parser = ConfigParser()
        default_parser.read("./src/EVA/defaults.ini")
        for section in default_parser:
            self.parser[section] = default_parser[section]
