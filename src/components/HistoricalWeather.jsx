import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

function HistoricalWeather({ selectedProvince }) {
  const [csvData, setCsvData] = useState([]);
  const [selectedYear, setSelectedYear] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    // Load and parse the CSV from the public folder
    Papa.parse(`${import.meta.env.BASE_URL}merged_climate_population.csv`, {
      download: true,
      header: true, 
      complete: (results) => {
        setCsvData(results.data);
      },
      error: (err) => {
        setError(err.message);
      },
    });
  }, []);

  const uniqueYears = Array.from(new Set(csvData.map(row => row.Year)))
    .filter(Boolean)
    .sort();

  const filteredData = csvData.filter(row => {
    const matchProvince = row.GEO === selectedProvince;
    const matchYear = selectedYear ? row.Year === selectedYear : true;
    return matchProvince && matchYear;
  });

  return (
    <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px' }}>
      <h2>Historical Weather Data for {selectedProvince} (1950-2023)</h2>
      
      {!selectedProvince && (
        <p>Please select a province to view historical data.</p>
      )}

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {selectedProvince && (
        <>
          {/* Year selection dropdown */}
          <div style={{ marginBottom: '15px' }}>
            <label htmlFor="yearSelect">Select Year : </label>
            <select
              id="yearSelect"
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
            >
              <option value="">-- All Years --</option>
              {uniqueYears.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>

          {/* Display filtered historical data in a table */}
          {filteredData.length > 0 ? (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ border: '1px solid #999', padding: '8px' }}>Province</th>
                  <th style={{ border: '1px solid #999', padding: '8px' }}>Year</th>
                  <th style={{ border: '1px solid #999', padding: '8px' }}>Mean Temp</th>
                  <th style={{ border: '1px solid #999', padding: '8px' }}>Max Temp</th>
                  <th style={{ border: '1px solid #999', padding: '8px' }}>Min Temp</th>
                  <th style={{ border: '1px solid #999', padding: '8px' }}>Population</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((row, index) => (
                  <tr key={index}>
                    <td style={{ border: '1px solid #999', padding: '8px' }}>{row.GEO}</td>
                    <td style={{ border: '1px solid #999', padding: '8px' }}>{row.Year}</td>
                    <td style={{ border: '1px solid #999', padding: '8px' }}>{row.Annual_Mean_Temp}</td>
                    <td style={{ border: '1px solid #999', padding: '8px' }}>{row.Annual_Max_Temp}</td>
                    <td style={{ border: '1px solid #999', padding: '8px' }}>{row.Annual_Min_Temp}</td>
                    <td style={{ border: '1px solid #999', padding: '8px' }}>{row.Population}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No historical data found for this selection.</p>
          )}
        </>
      )}
    </div>
  );
}

export default HistoricalWeather;
