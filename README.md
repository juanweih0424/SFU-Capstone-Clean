# SFU-Capstone-Clean

This project is a Climate Data Visualization Platform built for the SFU Capstone project. It consists of multiple components for analyzing, visualizing, and interacting with historical and predicted climate data across Canadian provinces.

---

## 🌦️ Weather App

The weather application, located in the root folder and built using **React** + **Vite**, allows users to:

- Select a province to view its historical temperature data (1950–2023).
- Filter by specific year or see trends across the entire time span.
- View charts and predictions based on processed climate data.

> Deployment is handled using GitHub Pages. Static resources are served from the `public/` directory.

---

## 🧹 Preprocess

The `preprocess/` folder contains Python scripts for:

- Cleaning raw datasets.
- Merging climate, population, and emissions data.
- Formatting them for frontend visualization and predictive modeling.

> These scripts ensure consistent data structure and quality for visual rendering and ML models.

---

## 📊 Output

The `output/` folder contains the results from the preprocessing stage:

- `merged_climate_population.csv` – Merged dataset used in the weather app.
- `ghgrp_emissions_1950_2023_predicted.csv` – Emissions predictions.
- Other supporting CSVs for population, z-scores, and emission summaries.

This folder is used by the React app for rendering graphs.

---

## 🔬 Analysis

The `analysis/` folder contains Python notebooks and scripts for:

- Exploring climate-emission relationships.
- Running time-series forecasting (e.g., ARIMA).
- Generating statistics, correlations, and visual insights.
- Performing predictive modeling (e.g., LSTM or RandomForestRegressor).

These provide deeper insights into climate trends and policy implications.

---

## 📁 Public

The `public/` folder includes:

- All static assets (e.g., images, CSVs) required at runtime.
- Files like `merged_climate_population.csv` are read by the frontend directly.

---

## 📦 How to Run Locally

1. Install dependencies:

   ```bash
   npm install

2. Run development server:

   ```bash
   npm run dev
   ```

## Github Page Deployment

https://juanweih0424.github.io/SFU-Capstone-Clean/

## Note: API key has expired and is now free trial so 7-day forecasting becomes 3-day AND I have removed source data from the directory since it creates problems with deploying the github pages
