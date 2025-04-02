import os
import pandas as pd
import matplotlib.pyplot as plt


input_path = r"D:\capstone project\output\ghgrp_emissions_1950_2023_predicted.csv"
output_dir = r"D:\capstone project\analysis\emissions_per_capita"
os.makedirs(output_dir, exist_ok=True)


df = pd.read_csv(input_path)
df = df.dropna(subset=['Province', 'Year', 'Population', 'Emissions'])


df['Emissions_per_Capita'] = df['Emissions'] / df['Population']


summary = df.groupby('Province')['Emissions_per_Capita'].agg(['mean', 'max', 'min']).reset_index()
summary = summary.sort_values('mean', ascending=False)


summary_path = os.path.join(output_dir, "emissions_per_capita_summary.csv")
summary.to_csv(summary_path, index=False)


trend_dir = os.path.join(output_dir, "trends")
os.makedirs(trend_dir, exist_ok=True)

for province in df['Province'].unique():
    sub = df[df['Province'] == province].sort_values('Year')
    plt.figure(figsize=(8, 4))
    plt.plot(sub['Year'], sub['Emissions_per_Capita'], marker='o')
    plt.title(f"{province} - Emissions per Capita Over Time")
    plt.xlabel("Year")
    plt.ylabel("Emissions per Capita (tonnes/person)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(trend_dir, f"{province}_emissions_per_capita.png"), dpi=150)
    plt.close()


plt.figure(figsize=(10, 6))
plt.bar(summary['Province'], summary['mean'], color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Average Emissions per Capita (tonnes/person)")
plt.title("Average Emissions per Capita by Province (1950–2023)")
plt.tight_layout()
bar_chart_path = os.path.join(output_dir, "mean_emissions_per_capita_bar_chart.png")
plt.savefig(bar_chart_path, dpi=150)
plt.close()

print("✅ Analysis Complete!")
print(f"📄 Summary CSV saved to: {summary_path}")
print(f"📈 Time-series trend plots saved in: {trend_dir}")
print(f"📊 Bar chart saved to: {bar_chart_path}")
