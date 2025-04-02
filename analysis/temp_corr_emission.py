import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


input_file = r"D:\capstone project\output\ghgrp_emissions_1950_2023_predicted.csv"
output_dir = r"D:\capstone project\analysis"
graph_dir = os.path.join(output_dir, "emissions_vs_temp_graphs")
os.makedirs(graph_dir, exist_ok=True)

df = pd.read_csv(input_file)

df = df.dropna(subset=['Province', 'Year', 'Annual_Mean_Temp', 'Emissions'])

results = []

for province in df['Province'].unique():
    sub = df[df['Province'] == province].copy().sort_values('Year')

    if len(sub) < 2:
        continue


    slope, intercept, r_value, p_value, std_err = linregress(
        sub['Annual_Mean_Temp'], sub['Emissions'])

    results.append({
        'Province': province,
        'Data_Points': len(sub),
        'Regression_Slope': slope,
        'Correlation_r': r_value,
        'p_value': p_value
    })


    plt.figure(figsize=(6, 4))
    plt.scatter(sub['Annual_Mean_Temp'], sub['Emissions'], alpha=0.6, label='Data')
    line = intercept + slope * sub['Annual_Mean_Temp']
    plt.plot(sub['Annual_Mean_Temp'], line, color='red', label=f"LinReg (r={r_value:.2f})")

    plt.title(f"{province} - Emissions vs Mean Temp")
    plt.xlabel("Annual Mean Temperature (°C)")
    plt.ylabel("Emissions (tonnes CO₂e)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()


    plot_path = os.path.join(graph_dir, f"{province}_emissions_vs_temp.png")
    plt.savefig(plot_path, dpi=150)
    plt.close()


summary_df = pd.DataFrame(results).sort_values(by='Correlation_r', ascending=False)
summary_path = os.path.join(output_dir, "emissions_temp_correlation_summary.csv")
summary_df.to_csv(summary_path, index=False)

print(f"✅ Analysis complete.")
print(f"📊 Summary CSV saved to: {summary_path}")
print(f"📈 Plots saved to: {graph_dir}")
