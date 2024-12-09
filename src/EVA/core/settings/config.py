from configparser import ConfigParser


class Config:
    """
    The Config class uses the python built-in module configparser to read and write configurations as .ini files.
    Configparser stores the config as a dictionary, which allows reading and writing to the configuration in memory.
    Any changes in the configuration can be saved to the file using the save_config() function.
    The configparser is stored under the 'parser' attribute of the Config class, but can also be accessed by indexing
    directly into the Config object.
    """
    def __init__(self):
        self.parser = ConfigParser()
        self.default_parser = ConfigParser()

    # This magic function allows the parser to be accessed when indexing directly into a config object:
    # Ex: it makes 'Config()["plot"]["fill_colour"]' equivalent to 'Config().parser["plot"]["fill_colour"]'
    def __getitem__(self, field: str):
        return self.parser[field]

    def load(self):
        self.default_parser = ConfigParser()
        self.default_parser.read("./src/EVA/core/settings/defaults.ini")

        # Try to load saved settings, if not found, create new config file and load default settings
        try:
            self.parser.read("./src/EVA/core/settings/config.ini")
        except FileNotFoundError:
            with open("./src/EVA/core/settings/config.ini", "w") as file:
                self.default_parser.write(file)
                file.close()

    def save_config(self):
        with open("./src/EVA/core/settings/config.ini", "w") as config_file:
            self.parser.write(config_file)
            config_file.close()

    def restore_defaults(self):
        for section in self.default_parser:
            self.parser[section] = self.default_parser[section]

    # checks if config loaded in memory is different to config in file
    def is_changed(self):
        temp_parser = ConfigParser()
        temp_parser.read("./src/EVA/core/settings/config.ini")

        for section in self.parser:
            if self.parser[section] != temp_parser[section]:
                return True # return True as soon as a difference is found
        return False

    # Splits space-separated string into an array. Ex: "1 2 3 4" -> ["1", "2", "3", "4"]
    def to_array(self, input_str):
        return input_str.split(" ")


