import json
import os


class ConfigManager:

    @staticmethod
    def get_config(config_type):
        root_path = os.getenv("NO_WAY_HOME_PATH")
        with open(f"{root_path}/config.json") as json_file:
            config_json = json.load(json_file)

        return config_json.get(config_type, None)


if __name__ == "__main__":
    db_config = ConfigManager.get_config("db")
    print(db_config)
