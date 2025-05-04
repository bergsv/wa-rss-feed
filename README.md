# World Archery Events RSS Feed

This repository automatically generates an RSS feed for upcoming and past events listed on the World Archery website.

## How it works

A Python script (`generate_feed.py`) fetches event data from the official World Archery API (`api.worldarchery.sport`) for the current year. It then generates an RSS feed file.

A GitHub Actions workflow (`.github/workflows/main.yml`) runs this script monthly. If the event data has changed, the workflow automatically updates the RSS feed file in the repository.

## Feed Location

The generated RSS feed is located at the root of this repository:

[`world_archery_events.xml`](./world_archery_events.xml)

You can use this URL directly in your RSS reader.

## Disclaimer & Contact

This project uses the publicly available World Archery API. It is intended for personal use and convenience.

If you encounter any issues with the feed, or if you believe this usage violates the terms of service of the World Archery API, please open an issue in this repository to contact the maintainer.
