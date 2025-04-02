import os
import glob
import pandas as pd


data_dir = r"D:\capstone project\data"
output_dir = r"D:\capstone project\output"


os.makedirs(output_dir, exist_ok=True)

file_pattern = os.path.join(data_dir, "*.csv")
file_list = glob.glob(file_pattern)

print(f"Found {len(file_list)} CSV files in {data_dir}.")


columns_to_keep = ["STATION", "NAME", "PRCP", "DATE", "SNOW", "TMIN", "TMAX"]


df_list = []

for file in file_list:
    try:

        df = pd.read_csv(file)
    except Exception as e:
        print(f"Error reading {file}: {e}")
        continue
    

    required_cols = {"TMIN", "TMAX"}
    if not required_cols.issubset(df.columns):
        print(f"Skipping {os.path.basename(file)} because it doesn't have TMIN or TMAX columns.")
        continue
    

    keep_these = [col for col in columns_to_keep if col in df.columns]
    df = df[keep_these]
    

    df = df.dropna(subset=["TMIN", "TMAX"])
    

    if not df.empty:
        df_list.append(df)


if df_list:
    final_df = pd.concat(df_list, ignore_index=True)
    print(f"Combined DataFrame has {len(final_df)} rows after cleaning.")
    
    output_file = os.path.join(output_dir, "cleaned_data.csv")
    final_df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to: {output_file}")
else:
    print("No valid data to combine after cleaning.")
