"""
A simple config manager that reads and writes key-value pairs from a file.
"""


class ConfigManager:
    def __init__(self, file_name, comment_char="#"):
        self.file_name = file_name
        self.comment_char = comment_char
        self.config_data = {}
        self.load_config()

    def load_config(self):
        with open(self.file_name, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith(self.comment_char):
                    # Skip empty lines and comments
                    continue
                parts = line.split("=")
                if len(parts) == 2:
                    config_key, config_value = parts[0].strip(), parts[1].strip()
                    # Remove double quotes around the value
                    config_value = config_value.strip('"')
                    self.config_data[config_key] = config_value

    def get_value(self, key):
        if key not in self.config_data:
            raise Exception(f"Key {key} is not found in config file {self.file_name}")

        return self.config_data.get(key)

    def set_value(self, key, value):
        self.config_data[key] = value
        self.write_config()

    def write_config(self):
        with open(self.file_name, "w") as file:
            for key, value in self.config_data.items():
                # Wrap the value in double quotes to handle spaces
                file.write(f'{key} = "{value}"\n')
