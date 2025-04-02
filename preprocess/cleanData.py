import pandas as pd


input_file = r"D:\capstone project\output\aggregateData.csv"
output_file = r"D:\capstone project\output\aggregateData_clean.csv"

df = pd.read_csv(input_file, parse_dates=["DATE"])

start_date = pd.to_datetime("1950-01-01")
end_date = pd.to_datetime("2024-12-31")
df_filtered = df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]

df_filtered["TMIN"] = df_filtered["TMIN"] / 10
df_filtered["TMAX"] = df_filtered["TMAX"] / 10

df_filtered["TAVG"] = ((df_filtered["TMIN"] + df_filtered["TMAX"]) / 2).round(2)


df_filtered.to_csv(output_file, index=False)

print(f"Filtered data with updated TMIN/TMAX and rounded TAVG saved to: {output_file}")
