""" This module is used to load the configuration file for the application. """
import json

def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

def get_connection_string():
    config = load_config()
    return (
        f"DRIVER={config['connection_string']['driver']};"
        f"SERVER={config['connection_string']['server']};"
        f"DATABASE={config['connection_string']['database']};"
        f"UID={config['connection_string']['username']};"
        f"PWD={config['connection_string']['password']}"
    )