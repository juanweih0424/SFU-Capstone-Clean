import pandas as pd
import os


temp_file = r"D:\capstone project\output\province_temperature_stats_zscore.csv"
pop_file = r"D:\capstone project\output\yearly_censusData.csv"
output_file = r"D:\capstone project\output\merged_climate_population.csv"


df_temp = pd.read_csv(temp_file)
df_pop = pd.read_csv(pop_file)


df_temp["Year"] = df_temp["Year"].astype(int)
df_pop["Year"] = df_pop["Year"].astype(int)

df_temp = df_temp[df_temp["Year"] < 2024]
df_pop = df_pop[df_pop["Year"] < 2024]


merged_df = pd.merge(df_temp, df_pop, on=["Year", "Province"], how="inner")


os.makedirs(os.path.dirname(output_file), exist_ok=True)
merged_df.to_csv(output_file, index=False)

print(f"✅ Merged dataset (without 2024) saved to: {output_file}")
