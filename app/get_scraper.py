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


if not db_host or not db_user or not db_pass or not db_sid:
    raise ValueError(
        "Please set TARGET_IP, DB_HOST, DB_USER, DB_PASS, and DB_SID in the .env file."
    )


def scrape_onu_data(target_ip):
    gecko_path = "/home/maestro/bin/geckodriver"
    s = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=s)

    try:
        driver.get(f"http://{target_ip}/#/login")
        wait = WebDriverWait(driver, 20)

        # Step 1: Login
        username = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        password = driver.find_element(By.XPATH, "//input[@type='password']")
        username.send_keys("root")
        password.send_keys("admin")
        password.send_keys(Keys.RETURN)

        onu_icon = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//i[contains(@class, 'iconfont icon-ONU')]")
            )
        )
        onu_icon.click()

        onu_mac_link = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//li[contains(@class, 'el-menu-item')]//span[text()='ONU MAC']",
                )
            )
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", onu_mac_link)
        onu_mac_link.click()

        table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".el-table"))
        )

        all_data = []

        current_page = 1

        while True:
            pager = driver.find_element(By.CSS_SELECTOR, ".el-pager")
            page_items = pager.find_elements(By.CSS_SELECTOR, "li.number")
            active_page = next(
                (
                    item.text
                    for item in page_items
                    if "active" in item.get_attribute("class")
                ),
                None,
            )

            if active_page == str(current_page):
                rows = table.find_elements(By.CSS_SELECTOR, ".el-table__body tr")
                columns = [
                    header.text
                    for header in table.find_elements(
                        By.CSS_SELECTOR, ".el-table__header th"
                    )
                ]

                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    data = [col.text for col in cols]
                    raw = dict(zip(columns, data))

                    cleaned = {
                        "OLT_ID": None,
                        "MAC": raw.get("MAC"),
                        "VLAN": raw.get("VLAN"),
                        "PORT": f"{raw.get('Port').replace(' ', '').upper()}:{raw.get('ONU')}",
                    }
                    all_data.append(cleaned)

                pager = driver.find_element(By.CSS_SELECTOR, ".el-pager")
                page_items = pager.find_elements(By.CSS_SELECTOR, "li.number")

                max_page = max([int(item.text) for item in page_items])

                if current_page == max_page:
                    break

                next_button = driver.find_element(By.CSS_SELECTOR, ".btn-next")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

                next_button.click()

                wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".el-table__body tr")
                    )
                )

                current_page += 1
            else:
                print(f"Waiting for page {current_page} to load...")
                wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, ".el-pager li.active"), str(current_page)
                    )
                )

        with open("scraper_output.json", "w") as f:
            json.dump(all_data, f, indent=4)
            print(f"{len(all_data)} Data saved to scraper_output.json")

    finally:
        driver.quit()
        return all_data


def main():
    parser = argparse.ArgumentParser(
        description="Process ONU data from SNMP output and insert into database"
    )
    parser.add_argument("-i", required=True, help="Target OLT IP address or hostname")
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Parse data but do not insert into database",
    )
    args = parser.parse_args()

    target_ip = args.i

    print("Scraping ONU data...")
    onu_data = scrape_onu_data(target_ip)
    print(f"Scraped {len(onu_data)} ONU devices from the web interface.")

    if not args.dry_run:
        print("Inserting data into database...")
        insert_into_db_olt_customer_mac(
            onu_data, target_ip, db_host, db_port, db_user, db_pass, db_sid
        )


if __name__ == "__main__":
    main()
