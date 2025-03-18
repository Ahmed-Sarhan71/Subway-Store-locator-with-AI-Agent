from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import sqlite3

# ✅ Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # Optional: Run in headless mode (no GUI)

# ✅ Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Open the Subway Malaysia "Find a Subway" page
url = "https://subway.com.my/find-a-subway"

try:
    driver.get(url)
    time.sleep(5)  # Wait for the page to load (increase if needed)
    
    # ✅ Check if the page contains expected content (like store locations)
    if not driver.find_elements(By.CLASS_NAME, "location_left"):
        raise Exception("❌ Error: Website loaded but no store data found. Structure may have changed.")

except Exception as e:
    print(f"❌ Error: Unable to access the Subway website. {e}")
    driver.quit()
    exit()  # Stop execution if website cannot be accessed

print("✅ Website is accessible. Proceeding with data extraction...")

# ✅ Find all store location divs
stores = driver.find_elements(By.CLASS_NAME, "location_left")

# ✅ Connect to SQLite database
conn = sqlite3.connect("subway_stores.db")
cursor = conn.cursor()

# ✅ Loop through each store to extract details and insert into database
for store in stores:
    try:
        store_name = store.find_element(By.TAG_NAME, "h4").text.strip()
        info_box = store.find_element(By.CLASS_NAME, "infoboxcontent")
        paragraphs = [p.text.strip() for p in info_box.find_elements(By.TAG_NAME, "p") if p.text.strip()]

        # ✅ Find corresponding "location_right" div for Waze link
        waze_link = "N/A"
        try:
            location_right = store.find_element(By.XPATH, "../div[@class='location_right']")
            waze_links = location_right.find_elements(By.TAG_NAME, "a")
            for link in waze_links:
                if "waze.com" in link.get_attribute("href"):
                    waze_link = link.get_attribute("href")
                    break
        except:
            pass  # No Waze link found

        # ✅ Ensure first paragraph contains "Kuala Lumpur" (valid address)
        if len(paragraphs) > 0 and "Kuala Lumpur" in paragraphs[0]:
            address = paragraphs[0]
            operating_hours = " | ".join(paragraphs[1:]).replace("\n", " ") if len(paragraphs) > 1 else "N/A"

            # ✅ Insert data into SQLite
            cursor.execute("""
                INSERT INTO subway_stores (store_name, address, operating_hours, waze_link)
                VALUES (?, ?, ?, ?)
            """, (store_name, address, operating_hours, waze_link))

            print(f"✅ Inserted: {store_name}")

    except Exception as e:
        print(f"⚠️ Error processing store: {e}")

# ✅ Commit and close database connection
conn.commit()
conn.close()

# ✅ Close WebDriver
driver.quit()

print("✅ Data successfully saved to database.")
