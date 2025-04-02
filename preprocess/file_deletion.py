'''File deletion: Delete all files that do not belong to Canada'''

import os
import glob


data_dir = r"D:\capstone project\data"


file_pattern = os.path.join(data_dir, "*.csv")
file_list = glob.glob(file_pattern)

print(f"Found {len(file_list)} CSV files in the directory.")

for file_path in file_list:
    file_name = os.path.basename(file_path)
    if not file_name.startswith("CA"):
        try:
            os.remove(file_path)
            print(f"Deleted: {file_name}")
        except Exception as e:
            print(f"Error deleting {file_name}: {e}")
    else:
        print(f"Kept: {file_name}")
