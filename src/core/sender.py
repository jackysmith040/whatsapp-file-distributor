import logging
import time
from typing import List, Dict, Any
from icecream import ic

# This now correctly imports the refactored backend
from src.core.sender_backends.selenium_sender import SeleniumSender
from config import DEFAULT_STAGGER_MINUTES

class WhatsAppFileSender:
    """High-level API for sending a queue of files via WhatsApp."""

    def __init__(self):
        self.backend = SeleniumSender()

    def initialize(self):
        """Initializes the backend browser."""
        # Corrected to call the actual method name in the backend
        self.backend.initialize_browser()

    def shutdown(self):
        """Shuts down the backend browser."""
        # Corrected to call the actual method name in the backend
        self.backend.shutdown_browser()

    def send_queue(self, queue: List[Dict[str, Any]]):
        """
        Processes and sends a queue of files with state-aware logic.
        """
        successful_sends, failed_sends = [], []
        current_group = None  # State variable to track the active chat

        for i, item in enumerate(queue):
            print("-" * 20)
            logging.info(
                f"Processing item {i + 1}/{len(queue)}: Send '{item['file_path'].name}' to '{item['group_name']}'"
            )

            target_group = item["group_name"]

            # --- State-Aware Logic ---
            if target_group != current_group:
                logging.info(f"Current group is '{current_group}'. Target is '{target_group}'. Switching chats.")
                if self.backend.select_chat(target_group):
                    current_group = target_group
                else:
                    logging.error(f"Skipping file for '{target_group}' as chat could not be selected.")
                    failed_sends.append(item)
                    current_group = None
                    continue
            else:
                logging.info(f"Target group '{target_group}' is already active. Skipping search.")

            # --- Send File ---
            if self.backend.attach_and_send_file(item["file_path"]):
                successful_sends.append(item)
            else:
                failed_sends.append(item)
                current_group = None # Reset state on failure to be safe

            if i < len(queue) - 1:
                wait_seconds = DEFAULT_STAGGER_MINUTES * 60
                logging.info(f"Waiting for {wait_seconds} seconds...")
                ic(f"Waiting for {wait_seconds} seconds...")
                time.sleep(wait_seconds)

        return successful_sends, failed_sends