import logging
import requests
from feedgen.feed import FeedGenerator
from datetime import datetime, date
import pytz
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_rss_feed():
    """Fetches World Archery events and generates an RSS feed file."""
    logging.info('Python script execution started.')

    try:
        # Aktuelles Datum für die API-Abfrage bestimmen
        current_date = datetime.now()
        current_year = current_date.year

        # Ersten Tag des Jahres bestimmen
        first_day = date(current_year, 1, 1)
        # Letzten Tag des Jahres bestimmen
        last_day = date(current_year, 12, 31)

        # API URL mit dem gesamten Jahr
        logging.info("Starting API query for the entire current year...")
        # Frage direkt 2000 Einträge ab
        url = f"https://api.worldarchery.sport/?EventTypeId=1&WorldRecordStatus=0&WorldRankingEvent=0&Cancelled=-1&Detailed=1&StartDate={first_day}&StopDate={last_day}&SortBy=DATE&v=3&content=COMPETITIONS&RBP=2000&LangID=EN"

        # Einmalige API-Anfrage
        logging.info(f"Fetching API: {url}")
        response = requests.get(url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        if 'items' not in data or not isinstance(data['items'], list):
            logging.warning("No items found or invalid format.")
            all_items = []
        else:
            all_items = data['items']
            logging.info(f"API query successful. Number of items: {len(all_items)}")

        logging.info("Creating RSS feed...")
        fg = FeedGenerator()
        fg.id('https://worldarchery.sport')
        fg.title('World Archery Events Feed')
        fg.author({'name': 'World Archery'})
        fg.link(href='https://www.worldarchery.sport/events/calendar', rel='alternate')
        fg.description('Current World Archery Events worldwide')
        fg.language('en')

        # Sort items by start date just in case the API doesn't guarantee it
        all_items.sort(key=lambda x: x.get('DFrom', '1970-01-01'))

        for item in all_items:
            title = item.get('Name', 'Unknown Event')
            location = f"{item.get('Place', 'Unknown Location')}, {item.get('CountryName', 'Unknown Country')}"
            start_date_str = item.get('DFrom', '1970-01-01')
            end_date_str = item.get('DTo', '1970-01-01')
            # Prefer Web link, fall back to Registration URL, then to general calendar
            link = item.get('Links', {}).get('Web') or item.get('Links', {}).get('Registration URL') or "https://www.worldarchery.sport/events/calendar"

            fe = fg.add_entry()
            fe.title(f"{title} ({start_date_str} – {end_date_str})")
            fe.link(href=link)
            description_parts = [
                f"Location: {location}",
                f"Level: {item.get('Level', 'Unknown')}",
                f"Status: {item.get('StatusDescription', 'Unknown')}"
            ]
            fe.description("
".join(description_parts))

            # Use the event ID as a unique identifier if available
            event_id = item.get('ID')
            if event_id:
                fe.id(f"urn:worldarchery:event:{event_id}")
            else:
                # Fallback ID generation (less ideal)
                 fe.id(f"urn:worldarchery:event:{title.replace(' ', '_')}:{start_date_str}")


            try:
                # Use a fixed timezone like UTC for consistency
                start_datetime = datetime.strptime(start_date_str, "%Y-%m-%d")
                fe.published(pytz.utc.localize(start_datetime))
            except ValueError:
                logging.warning(f"Invalid start date format for event: {title}. Using default.")
                fe.published(pytz.utc.localize(datetime(1970, 1, 1)))

        # Save RSS feed to the current directory
        output_file = 'world_archery_events.xml'
        logging.info(f"Saving RSS feed to file: {output_file}")
        fg.rss_file(output_file, pretty=True) # Use pretty=True for readability
        logging.info("RSS feed successfully created and saved.")

        logging.info('Processing completed successfully.')

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise
    except Exception as e:
        logging.error(f'Error occurred during execution: {e}')
        raise # Re-raise the exception so the GitHub Action fails

if __name__ == "__main__":
    generate_rss_feed()
    logging.info('Python script execution completed.') 