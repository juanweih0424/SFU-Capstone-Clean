// src/components/Weather.jsx
import React, { useState } from 'react';
import './Weather.css';
import HistoricalWeather from './HistoricalWeather';
import Prediction from './Prediction';

const provinceCityMapping = [
  { province: "Ontario", city: "Toronto" },
  { province: "Quebec", city: "Montreal" },
  { province: "British Columbia", city: "Vancouver" },
  { province: "Alberta", city: "Calgary" },
  { province: "Saskatchewan", city: "Regina" },
  { province: "Nova Scotia", city: "Halifax" },
  { province: "New Brunswick", city: "Moncton" },
  { province: "Newfoundland and Labrador", city: "St. John's" },
];

function Weather() {
  const [selectedCity, setSelectedCity] = useState("");
  const [selectedProvince, setSelectedProvince] = useState("");
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getDayOfWeek = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { weekday: 'short' });
  };

  const handleCityChange = async (event) => {
    const city = event.target.value;
    setSelectedCity(city);

    const found = provinceCityMapping.find((item) => item.city === city);
    setSelectedProvince(found ? found.province : "");

    if (!city) {
      setForecast(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const days = 7;
      const apiKey = "e378d0c44a314e1ea3340322251903";
      const url = `https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${encodeURIComponent(city)}&days=${days}&aqi=no&alerts=no`;

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Error fetching forecast for ${city}: ${response.statusText}`);
      }
      const data = await response.json();
      setForecast(data);
    } catch (err) {
      setError(err.message);
      setForecast(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="major-cities-weather">
      <h1>Weather & 7-Day Forecast</h1>

      {/* City selection dropdown */}
      <select value={selectedCity} onChange={handleCityChange}>
        <option value="">-- Select a city --</option>
        {provinceCityMapping.map(({ province, city }) => (
          <option key={city} value={city}>
            {province} - {city}
          </option>
        ))}
      </select>

      {/* Loading & error messages */}
      {loading && <p>Loading forecast data...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {/* Display forecast if available */}
      {forecast && !loading && !error && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px' }}>
          <h2>
            {forecast.location?.name}, {forecast.location?.region}
          </h2>

          {/* Current Weather in a horizontal flex container */}
          <div className="currentWeather">
            <h3>Current Weather</h3>
            <div className="currentDetails">
              <p>Temperature: {forecast.current?.temp_c} °C</p>
              <p>Condition: {forecast.current?.condition?.text}</p>
              <p>Humidity: {forecast.current?.humidity}%</p>
              <p>Wind: {forecast.current?.wind_kph} kph</p>
            </div>
          </div>

          {/* 7-Day Forecast */}
          <h3>7-Day Forecast</h3>
          <div className="forecast">
            {forecast.forecast?.forecastday?.map((day) => (
              <div
                key={day.date}
                style={{
                  minWidth: '100px',
                  textAlign: 'center',
                  border: '1px solid #ddd',
                  padding: '10px',
                }}
              >
                <p style={{ fontWeight: 'bold' }}>{getDayOfWeek(day.date)}</p>
                <p>{day.date}</p>
                <img
                  src={`https:${day.day?.condition?.icon}`}
                  alt={day.day?.condition?.text}
                  style={{ width: '50px', height: '50px' }}
                />
                <p>
                  {Math.round(day.day?.mintemp_c)}°C / {Math.round(day.day?.maxtemp_c)}°C
                </p>
                <p>{day.day?.condition?.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Historical Weather Component */}
      <HistoricalWeather selectedProvince={selectedProvince} />
      <Prediction selectedProvince={selectedProvince}/>
    </div>
  );
}

export default Weather;
