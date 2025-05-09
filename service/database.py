import json

database_path = "data/database.json"

def load_database():
    with open(database_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_database(database: dict):
    with open(database_path, "w", encoding="utf-8") as file:
        json.dump(database, file, indent=6)