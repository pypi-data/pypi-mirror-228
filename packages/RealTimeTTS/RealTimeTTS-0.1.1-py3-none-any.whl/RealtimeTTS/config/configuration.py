class Configuration:

    def __init__(self, engine_name):
        # Load configuration parameters based on engine name.
        # These can be default parameters or read from an external config file.
        self.params = self.load_config(engine_name)

    def load_config(self, engine_name):
        # Logic to load engine-specific config
        pass