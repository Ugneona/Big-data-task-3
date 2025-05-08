import pandas as pd
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
import logging

# Logging (helps to track at what point is the process(or at which point there is an error) and saves the process into a txt file)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insert_log.txt"),
        logging.StreamHandler()
    ]
)

# MongoDB connection function (uses mongos router on port 27020(local host))
def insert_chunk(chunk):
    try:
        client = MongoClient("mongodb://localhost:27020")
        db = client['ais']
        collection = db['raw_data']
        collection.insert_many(chunk.to_dict('records'))
        logging.info(f"Inserted chunk of size {len(chunk)}")
        client.close()
    except Exception as e:
        logging.error(f"Error inserting chunk: {e}")


#Prepare the CSV File:
#in Terminal run:
# pip install pandas pymongo
# wget http://web.ais.dk/aisdata/aisdk-2024-05-01.zip
# unzip aisdk-2024-05-01.zip
# Read CSV and insert in parallel
def main():
    file_path = "aisdk-2024-05-01-sampled.csv"  # We don't have the 2023-05-01 data right now
    chunks = pd.read_csv(file_path, chunksize=10000)
    with ThreadPoolExecutor(max_workers=6) as executor: #edit the worker count according to pc
        executor.map(insert_chunk, chunks)

if __name__ == "__main__":
    main()