from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from db import get_db_connection
import time

 
BASE_URL = "https://www.sydney.com"
EVENTS_URL = urljoin(BASE_URL, "/events")
 


def scrape_events():
    # Setup headless Chrome driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    print("EVENTS_URL:", EVENTS_URL)

    driver.get(EVENTS_URL)
    driver.implicitly_wait(10)  # wait for JS to load

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    event_tiles = soup.find_all("div", class_="grid-item product-list-widget tile__product-list")

    events = []

    for tile in event_tiles:
        try:
            # Event URL
            a_tag = tile.find("a", class_="tile__product-list-link")
            url = a_tag['href'] if a_tag and 'href' in a_tag.attrs else ""

            # Title
            title_tag = tile.find("div", class_="tile__product-list-tile-heading")
            title = title_tag.find("h3").get_text(strip=True) if title_tag else ""

            # Location
            location_tag = tile.find("div", class_="tile__product-list-area")
            location = location_tag.find("span", class_="tile__area-name").get_text(strip=True) if location_tag else ""

            # Description
            desc_tag = tile.find("div", class_="prod-desc")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            # Dates
            start_date_tag = tile.find("time", class_="start-date")
            start_date = start_date_tag.get_text(strip=True) if start_date_tag else ""

            end_date_tag = tile.find("time", class_="end-date")
            end_date = end_date_tag.get_text(strip=True) if end_date_tag else ""

            # Image URL
            image_div = tile.find("div", class_="tile__product-list-image")
            img_tag = image_div.find("img") if image_div else None
            img_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""

            events.append((title, location, description, start_date, end_date, url, img_url))

        except Exception as e:
            print(f"Error while parsing event tile: {e}")
            continue

    return events




CATEGORY_KEYWORDS = {
    "Tech": ["tech", "AI", "ML", "data", "cloud", "cybersecurity", "python", "blockchain","React"],
    "Music": ["concert", "music", "band", "dj", "orchestra", "singer"],
    "Art": ["art", "painting", "gallery", "exhibition"],
    "Business": ["startup", "entrepreneur", "business", "marketing", "sales"],
    "Health": ["yoga", "meditation", "health", "fitness", "wellness"],
    "Education": ["workshop", "seminar", "course", "training", "bootcamp"],
    "Sports": ["cricket", "football", "sports", "tournament", "run", "marathon"]
}

'''
def categorize_event(title):
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return "Other"
'''
def categorize_event(title):
    title_lower = title.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for kw in keywords if kw in title_lower)

    best_category = max(scores.items(), key=lambda x: x[1])[0]

    return best_category if scores[best_category] > 0 else "Other"


def scrape_pune_events():
    EVENTBRITE_PUNE_URL = "https://www.eventbrite.com/d/india--pune/events--this-week/"
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    print("Scraping:", EVENTBRITE_PUNE_URL)
    driver.get(EVENTBRITE_PUNE_URL)
    time.sleep(5)  # Let JS load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    events = []

    cards = soup.find_all("section", class_="discover-vertical-event-card")
    
    for card in cards:
        try:
            title_tag = card.find("h3")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            date_tag = card.find("p", string=lambda text: text and "AM" in text or "PM" in text)
            date = date_tag.get_text(strip=True) if date_tag else "N/A"

            location_tag = card.find("p", class_="event-card__clamp-line--one")
            location = location_tag.get_text(strip=True) if location_tag else "Pune"

            price_tag = card.find("div", class_="DiscoverVerticalEventCard-module__priceWrapper___usWo6")
            price = price_tag.get_text(strip=True) if price_tag else "Free"

            link_tag = card.find("a", class_="event-card-link")
            url = link_tag['href'] if link_tag else "#"

            image_tag = card.find("img", class_="event-card-image")
            img_url = image_tag["src"] if image_tag else ""

            #filter based on category  
            category = categorize_event(title)

            events.append((title, location, price, date, url, img_url,category))
        except Exception as e:
            print("Error parsing card:", e)

    return events


def save_events_to_db(events):
    conn = get_db_connection()       
    cur = conn.cursor()

    for event in events:
        cur.execute("""
            INSERT IGNORE INTO events (title, location, description, start_date, end_date, url, img_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, event)
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(events)} events into the database.")


def save_pune_events_to_db(events):
    conn = get_db_connection()
    cur = conn.cursor()

    for event in events:
        print("Event tuple:", event)
        print("Length of event:", len(event))  # Should be 7

        cur.execute("""
            INSERT IGNORE INTO events_pune (title, location, price, date, url, img_url,category )
            VALUES (%s, %s, %s, %s, %s, %s,%s)
        """, event)

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(events)} Pune events into the database.")

