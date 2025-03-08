import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

datasets = []
num_pages = 200
max_retries = 3  # Maximum number of retries per page

for page in range(1, num_pages + 1):
    url = f"https://catalog.data.gov/dataset/?page={page}"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='dataset-content')

                for item in items:
                    try:
                        title = item.find('h3').text.strip()
                        link = "https://catalog.data.gov" + item.find('h3').find('a')['href']
                        datasets.append({"title": title, "link": link})
                    except Exception as e:
                        print(f"Error processing item on page {page}: {e}")
                        continue

                print(f"Page {page} scraped successfully")
                break  # Exit the retry loop on success

            else:
                print(f"Error loading page {page}: Status code {response.status_code}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1) + random.uniform(0, 1)
                    time.sleep(wait_time)

        except requests.exceptions.RequestException as e:
            print(f"Request failed on page {page}, attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** (attempt + 1) + random.uniform(0, 1)
                time.sleep(wait_time)
    else:
        print(f"Failed to scrape page {page} after {max_retries} attempts")
        continue  # Proceed to the next page if all retries fail

    time.sleep(2 + random.random())  # Respectful crawling delay

# Save data to CSV
df = pd.DataFrame(datasets)
df.to_csv("datasets_data_gov.csv", index=False, encoding='utf-8-sig')

print(f"Successfully saved {len(datasets)} datasets to datasets_data_gov.csv")