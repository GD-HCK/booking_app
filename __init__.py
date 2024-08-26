import json

def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()

def get_connection_string():
    return (
        f"DRIVER={config['connection_string']['driver']};"
        f"SERVER={config['connection_string']['server']};"
        f"DATABASE={config['connection_string']['database']};"
        f"UID={config['connection_string']['username']};"
        f"PWD={config['connection_string']['password']}"
    )

def get_sqlalchemy_connection_string():
    return f'mssql+pyodbc://{config['connection_string']['username']}:{config['connection_string']['password']}@{config['connection_string']['server']}/{config['connection_string']['database']}?driver={config['connection_string']['driver'].replace(" ", "+")}'
