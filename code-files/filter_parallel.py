from pymongo import MongoClient
from datetime import datetime
from multiprocessing import Pool, cpu_count
import csv

def get_collection():
    client = MongoClient("mongodb://localhost:27020")
    db = client['ais']
    return db['filtered_data']

def process_mmsi(args):
    """Apdoroja vieną MMSI ir grąžina timestamp delta sąrašą"""
    mmsi, idx, total = args
    print(f"[{idx} / {total}] MMSI: {mmsi}")

    collection = get_collection()
    docs = list(collection.find({"MMSI": mmsi}).sort("# Timestamp", 1))

    if len(docs) < 2:
        return []

    deltas = []
    for i in range(1, len(docs)):
        t1 = docs[i-1]['# Timestamp']
        t2 = docs[i]['# Timestamp']

        if isinstance(t1, str):
            t1 = datetime.strptime(t1, "%d/%m/%Y %H:%M:%S")
        if isinstance(t2, str):
            t2 = datetime.strptime(t2, "%d/%m/%Y %H:%M:%S")

        delta = (t2 - t1).total_seconds()
        deltas.append(delta)

    return deltas

def get_all_unique_mmsi():
    collection = get_collection()
    return collection.distinct("MMSI")

def save_to_csv(data, filename="timestamp_deltas.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp Delta (seconds)"])
        for delta in data:
            writer.writerow([delta])

def main():
    mmsi_list = get_all_unique_mmsi()
    total = len(mmsi_list)

    # Paruošiame argumentus su pozicija (idx)
    args = [(mmsi, idx + 1, total) for idx, mmsi in enumerate(mmsi_list)]

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_mmsi, args)

    flat_result = [delta for sublist in results for delta in sublist]

    print(f"Iš viso apskaičiuota {len(flat_result)} timestamp skirtumų.")
    save_to_csv(flat_result)

    return flat_result

if __name__ == "__main__":
    main()
