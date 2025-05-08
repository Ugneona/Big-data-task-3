#relevant libraries
from pymongo import MongoClient
from datetime import datetime
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt

#function to get filtered data
def get_collection():
    client = MongoClient("mongodb://localhost:27020")
    db = client['ais']
    return db['filtered_data']

#function to count time differences between points for unique vessel, this function return time differences in a list
def process_mmsi(mmsi):
    collection = get_collection()
    docs = list(collection.find({"MMSI": mmsi}).sort('# Timestamp', 1))#findinge the correct mmsi and sorting by timestamp variable

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

#find all distinct mmsi numbers
def get_all_unique_mmsi():
    collection = get_collection()
    return collection.distinct("MMSI")


#this function plots histograms with various range and bin numbers, to see the full view of histogram and zoomed in
def plot_all_histograms(data):
    
    plt.figure()
    plt.hist(data, edgecolor='black')
    plt.xlabel('Time delta')
    plt.ylabel('Frequency')
    plt.title('Full time delta histogram', fontweight='bold')
    plt.grid(True)
    plt.savefig("hist_full.pdf", format="pdf")
    plt.show()
    plt.close()

    
    plt.figure()
    plt.hist(data, range=[0, 1000], bins=40, edgecolor='black')
    plt.xlabel('Time delta')
    plt.ylabel('Frequency')
    plt.title('Time delta histogram (0–1000s)', fontweight='bold')
    plt.grid(True)
    plt.savefig("hist_1000.pdf", format="pdf")
    plt.show()
    plt.close()

    
    plt.figure()
    plt.hist(data, range=[0, 100], bins=40, edgecolor='black')
    plt.xlabel('Time delta')
    plt.ylabel('Frequency')
    plt.title('Time delta histogram (0–100s)', fontweight='bold')
    plt.grid(True)
    plt.savefig("hist_zoom100.pdf", format="pdf")
    plt.show()
    plt.close()

    
    plt.figure()
    plt.hist(data, range=[0, 20], bins=10, edgecolor='black')
    plt.xlabel('Time delta')
    plt.ylabel('Frequency')
    plt.title('Time delta histogram (0–20s)', fontweight='bold')
    plt.grid(True)
    plt.savefig("hist_zoom20.pdf", format="pdf")
    plt.show()
    plt.close()

# the main function, which finds time delta for each mmsi using multiprocessing capabilities
def main():
    mmsi_list = get_all_unique_mmsi()
    total = len(mmsi_list)
    flat_result = []
    processed = 0

    print(f"Starting to count time delta for ({total} MMSI)...")

    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap_unordered(process_mmsi, mmsi_list):
            flat_result.extend(result)
            processed += 1
            print(f"Already finished MMSI: {processed} out of {total}")

    print(f"Making histograms...")
    plot_all_histograms(flat_result)


if __name__ == "__main__":
    result = main()
