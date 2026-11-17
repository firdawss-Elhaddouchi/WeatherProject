# Weather Desktop App

A Python desktop application for searching a city's weather and exploring current conditions, multi-day forecasts, and hourly temperatures.

## Features

- City search with weather descriptions and condition icons.
- Current temperature, humidity, and wind information.
- A detailed weather window with multi-day forecast entries.
- Hourly temperature information for the current day.
- A custom PyQt5 interface with bundled image assets.

## How it works

`App_weather.py` starts the application and handles city lookup. It opens `SecondWindow` from `weather.py` for detailed forecasts.

The application requests current weather and forecasts from OpenWeatherMap. It also uses Open-Meteo for hourly temperatures and weather codes.

## Run locally

Clone the repository and open a terminal in its root directory.

```powershell
git clone https://github.com/firdawss-Elhaddouchi/WeatherProject.git
cd WeatherProject
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install PyQt5 requests python-dotenv numpy
```

Create a local `.env` file in the repository root containing your own OpenWeatherMap API key.

```dotenv
API_KEY=your_openweathermap_api_key
```

Start the application from the root directory so relative image paths resolve correctly.

```powershell
python App_weather.py
```

A desktop environment and an internet connection are required.

## Repository structure

- `App_weather.py` — application entry point and city search.
- `weather.py` — detailed weather and forecast window.
- `images/` — interface backgrounds, icons, and other image assets.

## Implementation notes

API requests currently run synchronously in the interface code. Slow responses can delay the interface, and API errors or unexpected response fields may require additional error handling. Dependencies are listed above from the source imports and have no pinned versions in this repository.
