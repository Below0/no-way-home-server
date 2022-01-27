import json
import os

class ConfigManager:

    @staticmethod
    def get_config(config_type):
        ROOT_PATH = os.getenv("NO_WAY_HOME_PATH")
        with open(f"{ROOT_PATH}/config.json") as json_file:
            db_config = json.load(json_file)

        return db_config.get(config_type, None)

        
if __name__ == "__main__":
    db_config = ConfigManager.get_config("db")
    print(db_config)