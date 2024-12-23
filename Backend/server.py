from Const import CHUNK_SIZE, USE_COLS, ID_THRESHOLD
from random import randint
import pandas as pd


class Server:


    def __init__(self):

        self.data = []
        self.ids = set()
    

    def upload_data(self, data):

        for data_chunk in pd.read_csv(data, chunksize=CHUNK_SIZE, usecols=USE_COLS, parse_dates=["Decision Date"]):

            records = data_chunk.to_dict('records')
            for score in records:

                if pd.isna(score["Decision Date"]):
                    score["Decision Date"] = None
                
                new_id = randint(1, ID_THRESHOLD)
                while new_id in self.ids:
                    new_id = randint(1, ID_THRESHOLD)
                
                self.ids.add(new_id)
                score["id"] = new_id

                
            self.data += records
        
    
    def get_data(self):

        return self.data