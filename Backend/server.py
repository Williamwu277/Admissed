from Const import CHUNK_SIZE, USE_COLS, ID_THRESHOLD
from random import randint
import pandas as pd


class Server:


    def __init__(self):

        pass
    

    def upload_data(self, data, ids):

        result = []
        all_ids = set(ids)
        

        for data_chunk in pd.read_csv(data, chunksize=CHUNK_SIZE, usecols=USE_COLS, parse_dates=["Decision Date"]):

            records = data_chunk.to_dict('records')
            for score in records:

                if pd.isna(score["Decision Date"]):
                    score["Decision Date"] = None
                
                new_id = randint(1, ID_THRESHOLD)
                while new_id in all_ids:
                    new_id = randint(1, ID_THRESHOLD)
                
                all_ids.add(new_id)
                score["id"] = new_id
                score["Year"] = str(score["Year"])

            result += records
        
        return result