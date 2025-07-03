from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
import json
import os
from dotenv import load_dotenv
import argparse
import json
from .utils import insert_into_db_olt_customer_mac

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_sid = os.getenv("DB_SID")


if not all([db_host, db_user, db_pass, db_sid]):
    raise ValueError(
        "Please set DB_HOST, DB_USER, DB_PASS, and DB_SID in the .env file."
    )


def setup_driver() -> webdriver.Firefox:
    """Initializes and returns a Selenium Firefox WebDriver."""
    print(f"Initializing GeckoDriver from: {GECKODRIVER_PATH}")
    s = Service(executable_path=GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=s)
    return driver


def login(driver: webdriver.Firefox, wait: WebDriverWait, target_ip: str):
    """Logs into the target device's web interface."""
    print(f"Navigating to http://{target_ip}/#/login")
    driver.get(f"http://{target_ip}/#/login")
    print("Logging in with credentials...")
    username_field = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
    )
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    username_field.send_keys("root")
    password_field.send_keys("admin")
    password_field.send_keys(Keys.RETURN)
    print("Login successful.")


def navigate_to_onu_mac_table(driver: webdriver.Firefox, wait: WebDriverWait):
    """Navigates from the dashboard to the ONU MAC table page."""
    print("Navigating to ONU MAC table...")
    onu_icon = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//i[contains(@class, 'iconfont icon-ONU')]")
        )
    )
    onu_icon.click()

    onu_mac_link = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'el-menu-item')]//span[text()='ONU MAC']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", onu_mac_link)
    onu_mac_link.click()
    print("Navigation to table complete.")


def scrape_table_data(driver: webdriver.Firefox, wait: WebDriverWait) -> list[dict]:
    """Scrapes all pages of the table and returns the data."""
    print("Locating data table...")
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".el-table")))
    all_data = []
    current_page = 1

    while True:
        print(f"Scraping page {current_page}...")
        # Wait for the table to potentially refresh with new page data
        time.sleep(1)  # A small static wait can help with dynamic tables

        rows = table.find_elements(By.CSS_SELECTOR, ".el-table__body tr")
        headers = [
            th.text
            for th in table.find_elements(By.CSS_SELECTOR, ".el-table__header th")
        ]

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            raw_data = {headers[i]: col.text for i, col in enumerate(cols)}

            # Clean and format the extracted data
            cleaned_entry = {
                "OLT_ID": None,
                "MAC": raw_data.get("MAC"),
                "VLAN": raw_data.get("VLAN"),
                "PORT": f"{raw_data.get('Port', '').replace(' ', '').upper()}:{raw_data.get('ONU')}",
            }
            all_data.append(cleaned_entry)

        # Pagination logic
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button.btn-next")
            if not next_button.is_enabled():
                print("Last page reached. No more pages to scrape.")
                break

            print("Clicking 'Next Page' button.")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            next_button.click()
            current_page += 1
            # Wait for the pager to reflect the new page number to avoid stale element issues
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "li.number.is-active"), str(current_page)
                )
            )
        except TimeoutException:
            print("Could not find an active next page button. Assuming end of table.")
            break
        except Exception:
            print("Could not find a 'Next Page' button. Assuming single-page table.")
            break

    return all_data


def scrape_site(target_ip: str) -> list[dict]:
    """Orchestrates the entire scraping process for a given IP."""
    driver = setup_driver()
    all_data = []
    try:
        wait = WebDriverWait(driver, 20)
        login(driver, wait, target_ip)
        navigate_to_onu_mac_table(driver, wait)
        all_data = scrape_table_data(driver, wait)

        # Save the output to a file
        with open("scraper_output.json", "w") as f:
            json.dump(all_data, f, indent=4)
            print(f"\nSuccess! {len(all_data)} records saved to scraper_output.json")

    except Exception as e:
        print(f"\nAn error occurred during scraping: {e}")
    finally:
        print("Closing the browser.")
        driver.quit()
    return all_data


def main():
    """Main function to handle command-line arguments and run the scraper."""
    parser = argparse.ArgumentParser(
        description="Scrape ONU MAC data from a web interface."
    )
    parser.add_argument("-i", required=True, help="Target OLT IP address or hostname")
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Scrape data but do not insert into the database",
    )
    args = parser.parse_args()

    print("--- Starting Web Scraper ---")
    onu_data = scrape_site(args.i)
    print(f"Scraping finished. Found {len(onu_data)} ONU devices.")

    if not args.dry_run:
        if onu_data:
            print("Inserting data into the database...")
            insert_into_db_olt_customer_mac(
                onu_data, args.i, db_host, db_port, db_user, db_pass, db_sid
            )
        else:
            print("No data was scraped, skipping database insertion.")
    else:
        print("Dry run mode: Data was not inserted into the database.")


if __name__ == "__main__":
    main()
