import pandas as pd
import numpy as np

file_path = "aisdk-2024-05-01.csv"  # We don't have the 2023-05-01 data right now
df = pd.read_csv(file_path)
print("data read")

def sample_percent(input_array, percent=20, seed=41):
    # Takes array, returns random sample of n percent of it

    np.random.seed(seed)
    sample_size = int(len(input_array) * (percent * 0.01))
    random_indices = np.random.choice(len(input_array), size=sample_size, replace=False)
    
    return input_array[random_indices]

def sample_df(df, percent=20, seed=41):
    # Takes df, returns sampled df based on MMSI

    mmsi_array = df['MMSI'].unique()
    sampled_array = sample_percent(mmsi_array, percent, seed)

    df_sampled = df[df['MMSI'].isin(sampled_array)].copy()

    print('Original size: ', len(df), 'Size after sampling:', len(df_sampled))
    print('Size reduced to the percent of the original: ', round((len(df_sampled) / len(df)) * 100, 2))

    return df_sampled

# Sample dataframe based on MMSI and load it to csv
sample_df(df).to_csv("aisdk-2024-05-01-sampled.csv", index=False)
