from toml_config.core import Config


class ConfigWrapper:
    def __init__(self, configuration: Config):
        self.configuration = configuration

    def save(self):
        self.configuration.save()

    def value(self, section_name, property_name):
        return self.configuration.get_section(section_name).get(property_name).value

    def set(self, kwargs):
        self.configuration.set(**kwargs)
