import pandas as pd
import numpy as np
import os


input_file = r"D:\capstone project\data\censusData.csv"
output_file = r"D:\capstone project\output\yearly_censusData.csv"


df = pd.read_csv(input_file)


df["REF_DATE"] = pd.to_datetime(df["REF_DATE"], errors="coerce")


df["Year"] = df["REF_DATE"].dt.year
df["Quarter"] = df["REF_DATE"].dt.quarter


missing_quarters = [(1950, 1), (1950, 2), (1950, 3), (1950, 4), (1951, 1), (1951, 2)]


canada_population = df[(df["GEO"] == "Canada") & df["Year"].isin([1950, 1951])]


province_population_1951_Q3 = df[(df["GEO"] != "Canada") & (df["Year"] == 1951) & (df["Quarter"] == 3)].copy()

canada_1951_Q3_pop = canada_population[(canada_population["Year"] == 1951) & (canada_population["Quarter"] == 3)]["VALUE"].values
if len(canada_1951_Q3_pop) == 0:
    raise ValueError("Missing Canada population for 1951-Q3!")  

canada_1951_Q3_pop = canada_1951_Q3_pop[0]  
province_population_1951_Q3["Share"] = province_population_1951_Q3["VALUE"] / canada_1951_Q3_pop
province_population_1951_Q3 = province_population_1951_Q3.dropna(subset=["Share"])  

new_rows = []
for (year, quarter) in missing_quarters:
    canada_pop_for_quarter = canada_population[(canada_population["Year"] == year) & (canada_population["Quarter"] == quarter)]["VALUE"].values
    if len(canada_pop_for_quarter) == 0:
        continue  

    for _, row in province_population_1951_Q3.iterrows():
        estimated_pop = row["Share"] * canada_pop_for_quarter[0] 


        if pd.isna(estimated_pop) or estimated_pop == 0:
            print(f"Warning: Missing population estimate for {row['GEO']} in {year}-Q{quarter}")
            continue  # Skip problematic values

        new_rows.append({
            "REF_DATE": pd.to_datetime(f"{year}-01-01"), 
            "GEO": row["GEO"],
            "VALUE": estimated_pop, 
            "Year": year
        })


new_rows_df = pd.DataFrame(new_rows)

df = pd.concat([df, new_rows_df], ignore_index=True)

df_yearly = df.groupby(["Year", "GEO"], as_index=False)["VALUE"].mean()


df_yearly["VALUE"] = df_yearly["VALUE"].replace(0, np.nan) 
df_yearly["VALUE"] = df_yearly["VALUE"].fillna(method="bfill").fillna(method="ffill")  
df_yearly["Population"] = df_yearly["VALUE"].round().astype(int)  
df_yearly = df_yearly.drop(columns=["VALUE"])


df_yearly.rename(columns={"REF_DATE": "Year"}, inplace=True)


province_map = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Nova Scotia": "NS",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Northwest Territories": "NT",
    "Nunavut": "NU",
    "Yukon": "YT",
    "Canada": "CA"
}
df_yearly["Province"] = df_yearly["GEO"].map(province_map)


df_yearly = df_yearly.sort_values(by=["Year", "GEO"], ascending=[True, True])


columns_to_drop = ["DGUID", "UOM", "UOM_ID", "SCALAR_FACTOR", "SCALAR_ID", 
                   "VECTOR", "COORDINATE", "STATUS", "SYMBOL", "TERMINATED", "DECIMALS"]
df_yearly = df_yearly.drop(columns=[col for col in columns_to_drop if col in df_yearly.columns], errors="ignore")


os.makedirs(os.path.dirname(output_file), exist_ok=True)
df_yearly.to_csv(output_file, index=False)

print(f"✅ Yearly census data saved to: {output_file}")
