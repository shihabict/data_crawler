import json
import os

import pandas as pd

from configs.app_config import DATA_PATH
from settings import BASE_DIR


class NewDataSet:
    def create_dataset(self, path):
        files = os.listdir(path)
        all_data = pd.DataFrame()
        for file in files:
            data = pd.read_json(f"{BASE_DIR}\{DATA_PATH}\{file}")
            data = data[['title', 'category', 'raw_text']]
            all_data = pd.concat([all_data, data], ignore_index=True)
            # print(0)
        all_data = all_data.drop_duplicates(keep=False).reset_index(drop=True)
        print(f"Data Shape : {all_data.shape}")
        file_path = r"F:\projects\scrapper\DATA\title.json"
        file_path_csv = r"F:\projects\scrapper\DATA\title.csv"
        all_data.to_csv(file_path_csv, encoding='utf-8', index=False)
        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(all_data.to_dict(orient='records'), file, indent=4, ensure_ascii=False)
        print(f"Save into F:\projects\scrapper\DATA\title.json")
        # json.dump(all_data.to_dict(orient='records'), open(f"{BASE_DIR}\DATA\title.json", "w"), indent=4,
        #           ensure_ascii=False)


if __name__ == '__main__':
    new_data = NewDataSet()
    path = f"{BASE_DIR}\{DATA_PATH}"
    new_data.create_dataset(path)
