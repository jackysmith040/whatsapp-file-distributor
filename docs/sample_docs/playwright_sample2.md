```python
# --- WhatsApp Automation Bot - Final Polished Version ---
#
# Description:
# This script automates sending personalized WhatsApp messages with PDF attachments.
#
# Core Features:
# - Reads data from an Excel file.
# - Creates a new, timestamped log file for each run.
# - Persists login session to avoid repeated QR code scanning.
# - Clicks the first search result and then verifies the contact in the chat header.
# - Uses a flexible verification check for Name or Phone.
# - Includes human-like delays to avoid detection.
# - Performs a "soft UI reset" on error without reloading the page.

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Page, Locator
from datetime import datetime
import pandas as pd
import random
import time
import os
import re

# --- 1. CONFIGURATION ---
# All user-configurable settings are grouped here for easy access.

# --- Mode and Path Settings ---
HEADLESS_MODE = True      # Set to False to watch the bot in action.
LOG_DIRECTORY = "logs"    # The folder where session logs will be saved.
EXCEL_FILE_PATH = 'list.xlsx'
USER_DATA_DIR = "firefox_user_data" # Folder to store the login session.

# *** Excel Column Names ***
# These must exactly match the column headers in your Excel file.
NAME_COLUMN = 'ADI SOYADI'
COMPANY_NAME_COLUMN = 'ŞİRKET ADI'
PHONE_NUMBER_COLUMN = 'TELEFON NO'
DEBT_INFO_COLUMN = 'TOPLAM BORÇ'
PDF_PATH_COLUMN = 'PDF_PATH'

# --- Message and Timing Settings ---
MESSAGE_TEMPLATE = "Sn. {name}, {company_name} Firmanıza ait {debt_info} TL tutarındaki ..."
DELAY_BETWEEN_MESSAGES_BASE = 5  # Base delay in seconds between messages.
DELAY_BETWEEN_MESSAGES_RANDOM = 5 # Random seconds to add to the base delay.

# *** 2. CORE AUTOMATION SETTINGS ***
# These define the bot's interaction patterns and are likely to change depending on WhatApp Web UI updates.
SELECTORS = {
    "search_box": 'div[aria-label="Arama metni giriş alanı"]',
    "first_search_result": "//*[@id='pane-side']/div/div/div/div[2]/div",
    "chat_header_title": '//*[@id="main"]/header/div[2]/div[1]/div/div/div/span[1]',
    "attach_button": 'button[title="Ekle"]',
    "document_menu_item": 'text="Belge"',
    "close_preview_button": "div[aria-label='Kapat']",
    "caption_box": 'div[aria-label="Başlık ekleyin"]',
    "send_button": 'div[aria-label="Gönder"]',
}

# These options attempt to set the browser's language and environment.
# WhatsApp Web's display language is often determined by the language settings of the linked phone and might override these settings. 
# If the UI appears in an unexpected language, check the phone's settings first.
CONTEXT_OPTIONS = {
    'ignore_https_errors': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'extra_http_headers': { 'Accept-Language': 'tr-TR,tr;q=0.9' }, ### Should match these with your phone's language settings.
    'timezone_id': 'Europe/Istanbul',
    'locale': 'tr-TR',
    'viewport': {'width': 1366, 'height': 768}
}


class WhatsAppBot:
    """
    Encapsulates all logic for the WhatsApp automation bot.
    """
    def __init__(self, config):
        """Initializes the bot with configuration and sets up session logging."""
        self.config = config
        self.page: Page = None
        self.context = None
        self.playwright = None
        self._setup_session_logging()

    def _setup_session_logging(self):
        """Creates a unique, timestamped log file for this specific run."""
        log_dir = self.config['log_directory']
        os.makedirs(log_dir, exist_ok=True) # Create the 'logs' folder if it doesn't exist.
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        session_log_file = os.path.join(log_dir, f"run_{timestamp}.txt")
        self.config['session_log_file'] = session_log_file
        print(f"Logging this session to: {session_log_file}")

    def _log_event(self, level, details, error_msg=""):
        """Appends a formatted record (SUCCESS or FAILURE) to the current session's log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level} - Name: {details['name']}, Company: {details['company_name']}, Phone: {details['phone_number']}"
        if error_msg:
            log_entry += f" - Error: {str(error_msg).replace(chr(10), ' ')}\n"
        else:
            log_entry += "\n"
        try:
            with open(self.config['session_log_file'], 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Could not write to log file: {e}")

    def _patient_click(self, locator: Locator, timeout=15000):
        """A robust click function that waits for an element to be visible and adds human-like delays."""
        locator.wait_for(state='visible', timeout=timeout)
        time.sleep(random.uniform(1.0, 1.5))
        locator.click()
        time.sleep(random.uniform(0.5, 1.0))

    def _load_data(self):
        """Loads, validates, and cleans data from the specified Excel file."""
        print(f"Reading data from '{self.config['excel_path']}'...")
        try:
            df = pd.read_excel(self.config['excel_path'], dtype=str)
            required_cols = [
                self.config['phone_col'], self.config['pdf_col'], self.config['name_col'],
                self.config['company_col'], self.config['debt_col']
            ]
            df.dropna(subset=required_cols, inplace=True)
            df = df[df[self.config['phone_col']].str.strip() != '']
            df = df[df[self.config['pdf_col']].str.strip() != '']
            if df.empty:
                print("No valid rows with phone numbers and PDF paths found.")
                return None
            print(f"Found {len(df)} rows to process.")
            return df
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return None

    def _launch_browser(self):
        """Launches the browser with a persistent session and configured settings."""
        self.playwright = sync_playwright().start()
        self.context = self.playwright.firefox.launch_persistent_context(
            user_data_dir=self.config['user_data_dir'],
            headless=self.config['headless_mode'],
            slow_mo=200,
            **CONTEXT_OPTIONS
        )
        self.page = self.context.pages[0]
        self.page.set_default_timeout(30000)

    def _login(self):
        """Navigates to WhatsApp and waits for the session to load, confirming login."""
        print("\nOpening WhatsApp Web...")
        self.page.goto("https://web.whatsapp.com/")
        print("Waiting for login from saved session...")
        try:
            # We consider the user logged in if the search box is visible.
            self.page.locator(SELECTORS["search_box"]).wait_for(timeout=120000)
            print("Login successful!")
            return True
        except PlaywrightTimeoutError:
            print("Login timeout. Please run with headless=False to scan the QR code.")
            return False

    def _reset_ui(self):
        """Performs a 'soft' UI reset by closing chat/previews and clearing search, avoiding a full page reload."""
        print("Attempting to reset UI state...")
        try:
            # Attempt to close a media preview window if it's open.
            self.page.locator(SELECTORS["close_preview_button"]).click(timeout=1000)
        except PlaywrightTimeoutError:
            pass # It's okay if this isn't there.
        try:
            # Pressing 'Escape' is a reliable way to exit a chat view.
            self.page.keyboard.press("Escape")
            time.sleep(1)
            self.page.locator(SELECTORS["search_box"]).fill("")
            print("UI state reset.")
        except Exception as e:
            print(f"Could not perform soft UI reset: {e}. Navigating home as a fallback.")
            self.page.goto("https://web.whatsapp.com/")

    def _clean_phone(self, phone_number: str) -> str:
        """Removes all non-digit characters (e.g., '+', ' ', '()') and returns the last 10 digits."""
        return re.sub(r'\D', '', phone_number)[-10:]

    def _send_message(self, details: dict):
        """
        Executes the core message sending logic for a single contact using the "Act then Verify" pattern.
        """
        # --- Step 1: ACT - Search for the contact and click the first result ---
        search_box = self.page.locator(SELECTORS["search_box"])
        self._patient_click(search_box)
        search_box.fill(details['phone_number'])
        
        first_result = self.page.locator(SELECTORS["first_search_result"]).first
        self._patient_click(first_result)
        
        # --- Step 2: VERIFY - Check the chat header to confirm the correct contact is open ---
        print("Verifying chat header...")
        chat_header = self.page.locator(SELECTORS["chat_header_title"])
        chat_header.wait_for(state="visible", timeout=10000)

        # To be extra safe, we check both the visible text and the hidden 'title' attribute.
        title_text = chat_header.get_attribute("title") or ""
        inner_text = chat_header.inner_text() or ""
        verification_text = f"{title_text} {inner_text}"
        
        if not verification_text.strip():
             raise ValueError("Chat header was found but it is empty; cannot verify.")

        # --- Step 3: PERFORM THE VERIFICATION CHECKS ---
        # A. Check if the phone number matches (after cleaning both).
        phone_found = self._clean_phone(details['phone_number']) in self._clean_phone(verification_text)

        # B. Check if the name from Excel is contained in the header text (case-insensitive).
        name_found = details['name'].lower() in verification_text.lower()
        
        # If any of the checks pass, we can safely proceed.
        if phone_found or name_found:
            print(f"✅ Header verified: '{verification_text}'. Proceeding to send.")
            
            # --- Step 4: PROCEED - Attach file, add caption, and send ---
            self._patient_click(self.page.locator(SELECTORS["attach_button"]))
            document_menu = self.page.locator(SELECTORS["document_menu_item"])
            with self.page.expect_file_chooser() as fc_info:
                self._patient_click(document_menu)
            fc_info.value.set_files(details['pdf_path'])

            personalized_message = self.config['message_template'].format(**details)
            self.page.locator(SELECTORS["caption_box"]).fill(personalized_message)
            self._patient_click(self.page.locator(SELECTORS["send_button"]))
        else:
            # If no checks pass, raise an error to be caught by the calling function.
            raise ValueError(f"Verification Failed: Chat header '{verification_text}' did not match expected details.")

    def _process_row(self, row_data):
        """Prepares data for a single row and orchestrates the sending process within a safety net."""
        details = {
            'name': str(row_data[self.config['name_col']]).strip(),
            'company_name': str(row_data[self.config['company_col']]).strip(),
            'phone_number': str(row_data[self.config['phone_col']]).strip(),
            'debt_info': str(row_data[self.config['debt_col']]).strip(),
            'pdf_path': str(row_data[self.config['pdf_col']]).strip()
        }
        
        print(f"Processing: {details['name']} ({details['company_name']})")

        # Pre-check: Ensure the PDF file exists before starting browser actions.
        if not os.path.exists(details['pdf_path']):
            self._log_event("FAILURE", details, error_msg="PDF file not found at source.")
            return

        # Safety Net: Try to send the message, but be ready to catch errors.
        try:
            self._send_message(details)
            print(f"✅ Successfully sent PDF to {details['name']}")
            self._log_event("SUCCESS", details)
        except (PlaywrightTimeoutError, ValueError) as e:
            # Catch specific, expected errors for clearer logging.
            error_message = f"Verification failed or element timed out: {e}"
            print(f"❌ {error_message}")
            self._log_event("FAILURE", details, error_msg=error_message)
            self._reset_ui()
        except Exception as e:
            # Catch any other unexpected errors.
            error_message = f"An unexpected error occurred: {e}"
            print(f"❌ {error_message}")
            self._log_event("FAILURE", details, error_msg=error_message)
            self._reset_ui()

    def run(self):
        """The main execution method that orchestrates all bot operations."""
        data = self._load_data()
        if data is None: return
            
        self._launch_browser()
        try:
            if not self._login(): return

            for index, row in data.iterrows():
                print(f"\n--- Processing Row {index + 1}/{len(data)} ---")
                self._process_row(row)
                
                wait_time = self.config['delay_base'] + random.uniform(0, self.config['delay_random'])
                print(f"Waiting {wait_time:.2f} seconds before next message...")
                time.sleep(wait_time)

            print("\n✅ All messages processed successfully.")
        finally:
            print("Closing browser context...")
            if self.context: self.context.close()
            if self.playwright: self.playwright.stop()

# --- 3. SCRIPT EXECUTION ---
# This block runs when the script is executed directly.
if __name__ == "__main__":
    # Gathers all configuration settings into a single dictionary.
    bot_config = {
        # General
        "headless_mode": HEADLESS_MODE,
        "user_data_dir": USER_DATA_DIR,
        "log_directory": LOG_DIRECTORY,
        "excel_path": EXCEL_FILE_PATH,
        # Columns
        "name_col": NAME_COLUMN,
        "company_col": COMPANY_NAME_COLUMN,
        "phone_col": PHONE_NUMBER_COLUMN,
        "debt_col": DEBT_INFO_COLUMN,
        "pdf_col": PDF_PATH_COLUMN,
        # Messaging
        "message_template": MESSAGE_TEMPLATE,
        "delay_base": DELAY_BETWEEN_MESSAGES_BASE,
        "delay_random": DELAY_BETWEEN_MESSAGES_RANDOM,
    }
    
    bot = WhatsAppBot(bot_config)
    bot.run()