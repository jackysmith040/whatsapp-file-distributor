import logging
import random
import time
from pathlib import Path
from typing import List
from icecream import ic
from playwright.sync_api import (
    sync_playwright,
    Playwright,
    BrowserContext,
    Page,
    Locator,
    TimeoutError as PlaywrightTimeoutError,
)
from config import USER_DATA_DIR, HEADLESS_MODE, SELECTORS, MESSAGE_CAPTION


# A new, stable selector for the main side panel
PANE_SIDE_SELECTOR = "div[data-testid='pane-side']"


class VerificationError(Exception):
    """Custom exception for when chat header verification fails."""

    pass


class SendError(Exception):
    """Custom exception for a failed send attempt."""

    pass


class PlaywrightSender:
    def __init__(self):
        self.playwright: Playwright | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        ic("PlaywrightSender object created.")

    def _locate_with_fallback(self, selector_keys: List[str]) -> Locator:
        # --- NEW: Precondition Check ---
        if not self.page:
            raise RuntimeError("Browser is not initialized. Cannot locate elements.")

        for selector in selector_keys:
            try:
                locator = self.page.locator(selector)
                locator.wait_for(state="visible", timeout=3000)
                return locator
            except PlaywrightTimeoutError:
                continue
        raise PlaywrightTimeoutError(
            f"Could not find a visible element for any of the provided selectors: {selector_keys}"
        )

    # ... (initialize_browser and shutdown_browser are unchanged) ...
    def initialize_browser(self):
        ic("Initializing browser...")
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR, headless=HEADLESS_MODE, slow_mo=500
        )
        self.page = self.context.pages[0]
        ic("Navigating to WhatsApp Web...")
        self.page.goto("https://web.whatsapp.com/")
        try:
            ic("Checking for existing login session...")
            self.page.wait_for_selector(SELECTORS["login_check"][0], timeout=15000)
            print("✅ Login successful from saved session!")
            ic("Login successful from saved session!")
        except PlaywrightTimeoutError:
            print("Please scan the QR code to log in. Waiting up to 2 minutes...")
            ic("Waiting for QR code scan...")
            try:
                self.page.wait_for_selector(SELECTORS["login_check"][0], timeout=120000)
                print("✅ QR code scanned. Login successful!")
                ic("QR code scanned. Login successful!")
            except PlaywrightTimeoutError:
                logging.error(
                    "Timeout: Failed to log into WhatsApp Web within 2 minutes."
                )
                raise ConnectionError(
                    "Could not log into WhatsApp Web. Please try again."
                )

    def shutdown_browser(self):
        ic("Shutting down browser...")
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()
        logging.info("Browser has been shut down.")

    def _navigate_to_group(self, group_name: str):
        """Finds, opens, and verifies the chat for a specific group."""
        # --- NEW: Precondition Check ---
        if not self.page:
            raise RuntimeError("Browser is not initialized. Cannot navigate.")

        ic(f"Navigating to group: '{group_name}'")
        search_box = self._locate_with_fallback(SELECTORS["search_box"])
        search_box.evaluate("element => element.innerHTML = ''")
        search_box.click()
        time.sleep(random.uniform(0.5, 1.0))
        search_box.fill(group_name)

        result_selectors = [
            s.format(name=group_name) for s in SELECTORS["search_result_by_name"]
        ]
        search_result_locator = self._locate_with_fallback(result_selectors)
        search_result_locator.click()

        ic("Verifying chat header...")
        header = self._locate_with_fallback(SELECTORS["chat_header_title"])
        header_text = header.inner_text()
        if header_text != group_name:
            error_msg = f"Verification Failed! Expected '{group_name}' but found '{header_text}'."
            self.page.keyboard.press("Escape")
            raise VerificationError(error_msg)
        ic(f"✅ Header verified for '{group_name}'.")

    def _attach_file(self, file_path: Path):
        """Attaches a file to the message compose box."""
        # --- NEW: Precondition Check ---
        if not self.page:
            raise RuntimeError("Browser is not initialized. Cannot attach file.")

        ic(f"Attaching file: {file_path.name}")
        attach_button = self._locate_with_fallback(SELECTORS["attach_button"])
        attach_button.click()
        document_button = self._locate_with_fallback(SELECTORS["document_button"])
        with self.page.expect_file_chooser() as fc_info:
            document_button.click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)

    def _add_caption_and_send(self):
        """Adds a caption and clicks the final send button."""
        # --- NEW: Precondition Check ---
        if not self.page:
            raise RuntimeError("Browser is not initialized. Cannot send message.")

        ic("Adding caption and sending...")
        caption_box = self._locate_with_fallback(SELECTORS["caption_box"])
        caption_box.fill(MESSAGE_CAPTION)
        send_button = self._locate_with_fallback(SELECTORS["send_button"])
        send_button.click()
        send_button.wait_for(state="hidden", timeout=15000)
        ic("✅ File sent successfully.")

    def send_file(self, file_path: Path, group_name: str, hour: int, minute: int):
        # ... (This method is unchanged, as it calls the others which now have checks) ...
        for attempt in range(2):
            try:
                ic(
                    f"Attempt {attempt + 1}/2 to send '{file_path.name}' to '{group_name}'"
                )
                self._navigate_to_group(group_name)
                self._attach_file(file_path)
                self._add_caption_and_send()
                return
            except (PlaywrightTimeoutError, VerificationError, Exception) as e:
                logging.warning(f"Attempt {attempt + 1} failed for '{group_name}': {e}")
                if attempt == 1:
                    raise SendError(
                        f"Failed to send to '{group_name}' after 2 attempts."
                    )
                if self.page:
                    self.page.keyboard.press("Escape")  # Defensive check
                time.sleep(3)
