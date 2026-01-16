from dotcop.data.load_dotcop_configuration import DotcopConfiguration


class ConfigHandler:
    def __init__(self):
        self.dotcop_conf = DotcopConfiguration()

    def load_dotcop_config(self):
        try:
            config = self.dotcop_conf.load_configfile()
        except Exception:
            raise
        return config
