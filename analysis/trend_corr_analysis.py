import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv('../output/merged_climate_population.csv')

df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Population'] = pd.to_numeric(df['Population'], errors='coerce')
df['Annual_Mean_Temp'] = pd.to_numeric(df['Annual_Mean_Temp'], errors='coerce')

df = df.dropna(subset=['GEO', 'Year', 'Population', 'Annual_Mean_Temp'])

output_dir = "../output/graphs"
os.makedirs(output_dir, exist_ok=True)  

provinces = df['GEO'].unique()
results = []

for province in provinces:
    sub = df[df['GEO'] == province].copy()
    sub = sub.sort_values('Year')

    if len(sub) < 2:
        continue

    slope, intercept, r_value, p_value, std_err = linregress(sub['Year'], sub['Annual_Mean_Temp'])


    corr = sub['Annual_Mean_Temp'].corr(sub['Population'])

    results.append({
        'Province': province,
        'Data_Points': len(sub),
        'Temp_Trend_Slope': slope,
        'Temp_Trend_pValue': p_value,
        'Temp_vs_Pop_Corr': corr
    })


    plt.figure(figsize=(6, 4))
    plt.scatter(sub['Year'], sub['Annual_Mean_Temp'], label='Mean Temp Data')
    y_pred = intercept + slope * sub['Year']
    plt.plot(sub['Year'], y_pred, color='red', label=f'LinReg (slope={slope:.4f})')

    plt.title(f"{province} - Mean Temp Trend")
    plt.xlabel("Year")
    plt.ylabel("Annual Mean Temp (°C)")
    plt.legend()
    plt.grid(True)

    filename = f"{province}_mean_temp_trend.png"
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')

    plt.close()

results_df = pd.DataFrame(results)
print("\nSummary of Temperature Trend & Correlation:")
print(results_df)

results_df_sorted = results_df.sort_values('Temp_Trend_Slope', ascending=False)
print("\nSorted by largest warming slope:")
print(results_df_sorted)

output_csv_path = "../output/corrleation_population_temp.csv"  
results_df_sorted.to_csv(output_csv_path, index=False)
print(f"\nSaved sorted results to {output_csv_path}")