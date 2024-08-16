import json

class DataManager:
    FILE_NAME = 'shopping_data.json'

    @staticmethod
    def save_data(data):
        with open(DataManager.FILE_NAME, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def load_data():
        try:
            with open(DataManager.FILE_NAME, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
