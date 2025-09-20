import logging
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from icecream import ic

from config import USER_DATA_DIR, HEADLESS_MODE, SELECTORS, MESSAGE_CAPTION


class SeleniumSender:
    def __init__(self):
        self.driver: webdriver.Chrome | None = None
        self.wait: WebDriverWait | None = None

    def initialize_browser(self):
        ic("Initializing Selenium browser...")
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-data-dir={Path(USER_DATA_DIR).resolve()}")
        if HEADLESS_MODE:
            options.add_argument("--headless=new")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get("https://web.whatsapp.com")
        print(
            "\n"
            + "=" * 50
            + "\n--- ACTION REQUIRED ---\nBrowser has been launched. Please log in to WhatsApp Web."
        )
        input("===> Once your chats are visible, press Enter in this terminal...")
        ic("Waiting for chat list to load...")
        search_box_by, search_box_selector = SELECTORS["search_box"]
        by = By.CSS_SELECTOR if search_box_by == "css" else By.XPATH
        self.wait.until(EC.presence_of_element_located((by, search_box_selector)))
        ic("WhatsApp login confirmed.")

    def shutdown_browser(self):
        ic("Shutting down browser...")
        if self.driver:
            self.driver.quit()

    def select_chat(self, group_name: str) -> bool:
        """Searches for and opens a specific chat. Returns True on success."""
        try:
            # --- Select Chat ---
            search_by_str, search_selector = SELECTORS["search_box"]
            by = By.CSS_SELECTOR if search_by_str == "css" else By.XPATH
            search_box = self.wait.until(
                EC.element_to_be_clickable((by, search_selector))
            )
            self.driver.execute_script("arguments[0].innerHTML = '';", search_box)
            search_box.click()
            search_box.send_keys(group_name)
            time.sleep(1.5)
            result_by_str, result_selector = SELECTORS["search_result_by_name"]
            by = By.CSS_SELECTOR if result_by_str == "css" else By.XPATH
            self.wait.until(EC.element_to_be_clickable((by, result_selector))).click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Could not find or click on chat '{group_name}'. Error: {e}")
            self.driver.get("https://web.whatsapp.com")  # Reset state on failure
            return False

    def attach_and_send_file(self, file_path: Path) -> bool:
        """Attaches and sends a file to the currently active chat. Returns True on success."""
        try:

            # Step 3: Click attach button
            ic(f"Preparing to send '{file_path.name}'...")
            attach_by_str, attach_selector = SELECTORS["attach_button"]
            by = By.CSS_SELECTOR if attach_by_str == "css" else By.XPATH
            self.wait.until(EC.element_to_be_clickable((by, attach_selector))).click()
            time.sleep(1)
            
            # --- Direct File Attachment and Send ---
            ic(f"Attaching '{file_path.name}' to active chat...")
            file_input_by_str, file_input_selector = SELECTORS["file_input"]
            by = By.CSS_SELECTOR if file_input_by_str == "css" else By.XPATH
            self.driver.find_element(by, file_input_selector).send_keys(
                str(file_path.resolve())
            )

            # caption_by_str, caption_selector = SELECTORS["caption_box"]
            # by = By.CSS_SELECTOR if caption_by_str == "css" else By.XPATH
            # caption_box = self.wait.until(
            #     EC.element_to_be_clickable((by, caption_selector))
            # )
            # caption_box.send_keys(MESSAGE_CAPTION)

            send_by_str, send_selector = SELECTORS["send_button"]
            by = By.CSS_SELECTOR if send_by_str == "css" else By.XPATH
            self.wait.until(EC.element_to_be_clickable((by, send_selector))).click()

            ic(f"✅ Send command issued for '{file_path.name}'")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(
                f"Could not attach or send file. A selector may be invalid. Error: {e}"
            )
            self.driver.get("https://web.whatsapp.com")  # Reset state on failure
            return False
