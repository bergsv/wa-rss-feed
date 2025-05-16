# World Archery Events Data

This repository automatically fetches event data from the official World Archery API and stores it as a JSON file.

## How it works

A Python script (`fetch_events.py`) fetches event data from the official World Archery API (`api.worldarchery.sport`) for the current year. It then saves this data into a `world_archery_data.json` file.

A GitHub Actions workflow (`.github/workflows/main.yml`) runs this script weekly. If the event data has changed, the workflow automatically updates the `world_archery_data.json` file in the repository.

## Data File Location

The generated JSON data file is located at the root of this repository:

[`world_archery_data.json`](./world_archery_data.json)

You can use the raw URL to this file (e.g., `https://raw.githubusercontent.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>/main/world_archery_data.json`) to access the data in your applications.

## Disclaimer & Contact

This project uses the publicly available World Archery API. It is intended for personal use and convenience.

If you encounter any issues with the data, or if you believe this usage violates the terms of service of the World Archery API, please open an issue in this repository to contact the maintainer.
