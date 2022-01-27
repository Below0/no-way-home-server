import json

class ConfigManager:

    @staticmethod
    def get_config(config_type):
        with open("./config.json") as json_file:
            db_config = json.load(json_file)

        return db_config.get(config_type, None)

        
