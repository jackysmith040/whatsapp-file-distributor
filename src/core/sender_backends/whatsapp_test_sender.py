import os
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple

# --- Selenium & Webdriver Manager Imports ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ----------------------------------------------------------------------
# --- CONFIGURATION (Edit this section) ---
# ----------------------------------------------------------------------

# 1. SET PERSISTENT SESSION PATH
USER_DATA_DIR = Path(__file__).parent / "chrome_session"

# 2. SET YOUR WORKSPACE FOLDER
DEFAULT_WORKSPACE = Path.home() / "Desktop"

# 3. DEFINE YOUR RULES
RULE_MAPPING = [
    {
        "keywords": ["system", "dynamical"],
        "target_groups": ["iampeace"],
    },
    {
        "keywords": ["end"],
        "target_groups": ["iampeace"],
    },
]

# 4. SET DELAY BETWEEN MESSAGES
STAGGER_SECONDS = 15

# 5. ⚠️ CENTRALIZED SELECTORS HUB (Updated with your XPaths) ⚠️
SELECTORS = {
    "search_box": ("xpath", '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p'),
    "chat_result": ("xpath", '//*[@id="pane-side"]/div[1]/div/div/div[2]/div/div/div/div[2]'),
    "attach_button": ("xpath", '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[1]/div/span/div/div/div[1]/div[1]/span'),
    "document_option": ("xpath", '//*[@id="app"]/div[1]/span[6]/div/ul/div/div/div[1]/li/div'),
    
    # --- UPDATED ---
    # Switched to an XPath selector for the file input.
    "document_input": ("xpath", "//input[@type='file']"),

    "send_button": ("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div/span'),
}

# ----------------------------------------------------------------------
# --- CORE LOGIC (No need to edit below this line) ---
# ----------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FolderReader:
    def __init__(self, workspace_path: Path):
        self.workspace = Path(workspace_path)
    def select_folder(self) -> Path | None:
        if not self.workspace.is_dir():
            logging.error(f"Workspace directory not found at '{self.workspace}'")
            return None
        sub_folders = sorted([f for f in self.workspace.iterdir() if f.is_dir()], key=lambda p: p.name)
        if not sub_folders:
            logging.info(f"No sub-folders found in the workspace: '{self.workspace}'")
            return None
        while True:
            print("\nPlease select a folder to process:")
            for i, folder in enumerate(sub_folders, 1): print(f"  [{i}] {folder.name}")
            try:
                choice_idx = int(input("Enter the number of your choice: ")) - 1
                if 0 <= choice_idx < len(sub_folders):
                    selected_path = sub_folders[choice_idx]
                    confirm = input(f"You selected '{selected_path.name}'. Process? (y/n): ").lower()
                    if confirm in ["y", "yes"]: return selected_path
                else: print("⚠️ Invalid number. Please try again.")
            except (ValueError, IndexError): print("⚠️ Invalid input. Please enter a valid number.")

class DispatcherController:
    def __init__(self, rule_mapping: List[Dict[str, Any]]):
        self.rule_mapping = rule_mapping
    def get_processed_queue(self, target_folder: Path) -> Tuple[List[Dict[str, Any]], List[Path]]:
        logging.info(f"Scanning for PDF files in '{target_folder.name}'...")
        pdf_files = [f for f in target_folder.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"]
        base_queue, unmatched_files = [], []
        for pdf_path in pdf_files:
            matched = False
            for rule in self.rule_mapping:
                if any(k.lower() in pdf_path.name.lower() for k in rule.get("keywords", [])):
                    for group_name in rule.get("target_groups", []):
                        base_queue.append({"file_path": pdf_path, "group_name": group_name})
                    matched = True
            if not matched: unmatched_files.append(pdf_path)
        logging.info(f"Found {len(pdf_files)} PDFs. {len(base_queue)} queue items created.")
        return base_queue, unmatched_files

class WhatsAppAutomation:
    def __init__(self, user_data_dir: Path):
        self.user_data_dir = user_data_dir
        self.driver = None
        self.wait = None
        self.init_driver()

    def init_driver(self):
        try:
            os.makedirs(self.user_data_dir, exist_ok=True)
            options = Options()
            options.add_argument(f"user-data-dir={self.user_data_dir.resolve()}")
            options.add_argument("--start-maximized")
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 20)
            self.driver.get("https://web.whatsapp.com")
            print("\n" + "="*50 + "\n--- BROWSER ACTION REQUIRED ---\nBrowser open. Log in if needed.")
            input("===> Once your chat list is visible, press Enter here...")
            logging.info("User confirmed WhatsApp is ready.")
        except Exception as e:
            logging.critical(f"Failed to initialize Selenium driver: {e}")
            raise

    def get_by(self, selector_key: str):
        selector_type, selector_str = SELECTORS[selector_key]
        return By.CSS_SELECTOR if selector_type == "css" else By.XPATH, selector_str

    def send_file_to_group(self, file_path: Path, group_name: str) -> bool:
        try:
            logging.info(f"Attempting to send '{file_path.name}' to '{group_name}'...")

            # Step 1: Search
            by, selector = self.get_by("search_box")
            search_box = self.wait.until(EC.presence_of_element_located((by, selector)))
            search_box.clear()
            search_box.send_keys(group_name)
            time.sleep(2)

            # Step 2: Click chat result
            by, selector = self.get_by("chat_result")
            self.wait.until(EC.element_to_be_clickable((by, selector))).click()
            time.sleep(2)

            ### --- FIX: Re-enabled the necessary clicks to reveal the file input --- ###
            # Step 3: Click attach button
            by, selector = self.get_by("attach_button")
            self.wait.until(EC.element_to_be_clickable((by, selector))).click()
            time.sleep(1)

            # # Step 4: Click the 'Document' icon
            # by, selector = self.get_by("document_option")
            # self.wait.until(EC.element_to_be_clickable((by, selector))).click()
            # time.sleep(1)
            
            # Step 5: Find the hidden file input and upload
            by, selector = self.get_by("document_input")
            self.driver.find_element(by, selector).send_keys(str(file_path.resolve()))
            time.sleep(2)

            # Step 6: Click the final send button
            by, selector = self.get_by("send_button")
            self.wait.until(EC.element_to_be_clickable((by, selector))).click()
            time.sleep(3)

            logging.info(f"✅ Successfully sent '{file_path.name}' to '{group_name}'.")
            return True
        except (TimeoutException, NoSuchElementException):
            logging.error(f"❌ FAILED: Could not find an element for '{group_name}'. Verify your XPaths.")
            return False
        except Exception as e:
            logging.error(f"❌ FAILED: An unexpected error occurred: {e}")
            return False

    def cleanup(self):
        if self.driver:
            logging.info("Closing Chrome browser.")
            self.driver.quit()

def main():
    logging.info("--- WhatsApp PDF Distributor v3.3 Started ---")
    folder_reader = FolderReader(workspace_path=DEFAULT_WORKSPACE)
    dispatcher = DispatcherController(rule_mapping=RULE_MAPPING)
    selected_folder = folder_reader.select_folder()
    if not selected_folder: return
    queue, unmatched = dispatcher.get_processed_queue(target_folder=selected_folder)
    if not queue:
        logging.info("Queue is empty. Nothing to send.")
        if unmatched: print("\nUnmatched files:", *[f.name for f in unmatched], sep="\n  - ")
        return
    print("\n--- Sending Plan ---")
    for item in queue: print(f"  - Send '{item['file_path'].name}' to '{item['group_name']}'")
    if input("\nProceed? (y/n): ").lower() not in ["y", "yes"]:
        print("Sending cancelled.")
        return
    sender = None
    try:
        sender = WhatsAppAutomation(user_data_dir=USER_DATA_DIR)
        successful_sends, failed_sends = 0, 0
        for i, item in enumerate(queue, 1):
            print("-" * 20)
            logging.info(f"Processing item {i}/{len(queue)}...")
            if sender.send_file_to_group(item["file_path"], item["group_name"]):
                successful_sends += 1
            else:
                failed_sends += 1
            if i < len(queue):
                logging.info(f"Waiting for {STAGGER_SECONDS} seconds...")
                time.sleep(STAGGER_SECONDS)
        print(f"\n--- Sending Complete ---\n✅ Successful: {successful_sends}\n❌ Failed: {failed_sends}")
    except Exception as e:
        logging.critical(f"A critical error occurred: {e}")
    finally:
        if sender: sender.cleanup()
        logging.info("--- Application Finished ---")

if __name__ == "__main__":
    main()