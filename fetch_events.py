import logging
import requests
from datetime import datetime, date
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

OUTPUT_FILENAME = "world_archery_data.json"

def fetch_and_save_events():
    """Fetches World Archery event data and saves it as a JSON file."""
    logging.info('Starting to fetch World Archery event data.')

    try:
        current_date = datetime.now()
        current_year = current_date.year
        first_day = date(current_year, 1, 1)
        last_day = date(current_year, 12, 31)

        url = f"https://api.worldarchery.sport/?EventTypeId=1&WorldRecordStatus=0&WorldRankingEvent=0&Cancelled=-1&Detailed=1&StartDate={first_day}&StopDate={last_day}&SortBy=DATE&v=3&content=COMPETITIONS&RBP=2000&LangID=EN"

        logging.info(f"Fetching API: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()

        if 'items' not in data or not isinstance(data['items'], list):
            logging.warning("No items found in API response or invalid format.")
            all_items = []
        else:
            all_items = data['items']
            logging.info(f"API query successful. Number of items fetched: {len(all_items)}")

        # Save the 'items' list to a JSON file
        logging.info(f"Saving event data to {OUTPUT_FILENAME}")
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(all_items, f, ensure_ascii=False, indent=4)
        logging.info(f"Event data successfully saved to {OUTPUT_FILENAME}")

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise
    except Exception as e:
        logging.error(f'Error occurred during fetching or saving event data: {e}')
        raise

if __name__ == "__main__":
    fetch_and_save_events()
    logging.info('fetch_events.py script execution completed.') 