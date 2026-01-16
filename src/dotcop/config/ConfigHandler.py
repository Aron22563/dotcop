from .ValidateConfigfile import ValidateConfigfile

class ConfigHandler:
    def __init__(self):
        self.dotcop_conf = ValidateConfigfile()

    def load_dotcop_config(self):
        try:
            config = self.dotcop_conf.load_configfile()
        except Exception:
            raise
        return config
