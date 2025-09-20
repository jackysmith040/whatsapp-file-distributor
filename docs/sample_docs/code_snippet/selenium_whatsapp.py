from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import tkinter as tk
from tkinter import ttk
import time
import random
import logging
from datetime import datetime
import pyperclip
from PIL import Image, ImageTk

# Configure logging
logging.basicConfig(
    filename=f'whatsapp_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class LoginConfirmation:
    def __init__(self):
        self.is_confirmed = False

    def create_popup(self):
        self.root = tk.Tk()
        self.root.title("WhatsApp Login Confirmation - @Apeli Solutions")

        # Increased window size
        window_width, window_height = 800, 800
        screen_width, screen_height = (
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight(),
        )
        center_x, center_y = (screen_width - window_width) // 2, (
            screen_height - window_height
        ) // 2

        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#121212")  # Dark theme background

        logo = Image.open("apelinifa.png")
        logo = logo.resize((90, 90), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(logo)

        # Main Frame
        frame = tk.Frame(self.root, bg="#1E1E1E", bd=2, relief="ridge")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header Section
        header_frame = tk.Frame(frame, bg="#1E1E1E")
        header_frame.pack(pady=10)
        logo_label = tk.Label(header_frame, image=self.logo_img, bg="#1E1E1E")
        logo_label.pack()
        ttk.Label(
            header_frame,
            text="@Apeli Solutions",
            font=("Helvetica", 14, "bold"),
            foreground="#3498DB",
            background="#1E1E1E",
        ).pack()

        # Card Container
        card = tk.Frame(frame, bg="#2C2C2C", padx=20, pady=20, relief="raised", bd=5)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(
            card,
            text="WhatsApp Web Login Status",
            font=("Helvetica", 16, "bold"),
            foreground="#FFFFFF",
            background="#2C2C2C",
        ).pack(pady=10)
        ttk.Label(
            card,
            text="Please confirm after you have successfully logged in to WhatsApp Web.",
            wraplength=450,
            font=("Helvetica", 12),
            foreground="#CCCCCC",
            background="#2C2C2C",
        ).pack(pady=5)

        # Steps for Automation
        steps_frame = tk.Frame(card, bg="#2C2C2C")
        steps_frame.pack(pady=10)
        steps = [
            "1. 📱 Open WhatsApp on your phone.",
            "2. 🔗 Tap 'Linked Devices' and scan the QR code.",
            "3. ⏳ Wait for the connection to establish.",
            "4. ✅ Click 'Confirm Login' to start automation.",
        ]

        for step in steps:
            step_card = tk.Frame(
                steps_frame, bg="#3A3A3A", padx=10, pady=5, relief="ridge", bd=3
            )
            step_card.pack(fill=tk.X, pady=5)
            ttk.Label(
                step_card,
                text=step,
                font=("Helvetica", 10),
                foreground="#A9A9A9",
                background="#3A3A3A",
            ).pack(anchor="w", pady=2)

        # Buttons
        button_frame = tk.Frame(card, bg="#2C2C2C")
        button_frame.pack(pady=10)

        self.confirm_button = tk.Button(
            button_frame,
            text="✅ Confirm Login & Start Automation",
            command=self.confirm_login,
            font=("Helvetica", 12, "bold"),
            bg="#3498DB",
            fg="white",
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            borderwidth=2,
        )
        self.confirm_button.pack(pady=10, ipadx=10, ipady=5)
        self.confirm_button.bind("<Enter>", self.on_hover_confirm)
        self.confirm_button.bind("<Leave>", self.on_leave_confirm)

        self.cancel_button = tk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.cancel_login,
            font=("Helvetica", 12, "bold"),
            bg="#E74C3C",
            fg="white",
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            borderwidth=2,
        )
        self.cancel_button.pack(ipadx=10, ipady=5)
        self.cancel_button.bind("<Enter>", self.on_hover_cancel)
        self.cancel_button.bind("<Leave>", self.on_leave_cancel)

        self.root.mainloop()

    # Button animations
    def on_hover_confirm(self, event):
        self.confirm_button.configure(bg="#2980B9")

    def on_leave_confirm(self, event):
        self.confirm_button.configure(bg="#3498DB")

    def on_hover_cancel(self, event):
        self.cancel_button.configure(bg="#C0392B")

    def on_leave_cancel(self, event):
        self.cancel_button.configure(bg="#E74C3C")

    def confirm_login(self):
        self.is_confirmed = True
        self.root.destroy()

    def cancel_login(self):
        self.is_confirmed = False
        self.root.destroy()


class WhatsAppAutomation:
    def __init__(self, chromedriver_path):
        self.setup_driver(chromedriver_path)
        self.wait = WebDriverWait(self.driver, 30)

    def setup_driver(self, chromedriver_path):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://web.whatsapp.com")
        logging.info("Browser initialized and navigated to WhatsApp Web")

    def wait_for_presence(self, by, value, timeout=30):
        """Wait for element to be present and return it"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            return None

    def wait_for_clickable(self, by, value, timeout=30):
        """Wait for element to be clickable and return it"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        except TimeoutException:
            return None

    def find_search_box(self):
        """Find the search box using multiple strategies"""
        search_selectors = [
            (By.CSS_SELECTOR, 'div[title="Search or start new chat"]'),
            (By.CSS_SELECTOR, 'div[data-tab="3"]'),
            (
                By.XPATH,
                '//div[@contenteditable="true"][@title="Search or start new chat"]',
            ),
            (By.XPATH, '//div[@title="Search input textbox"]'),
            (By.CSS_SELECTOR, '[data-testid="chat-list-search"]'),
        ]

        for by, selector in search_selectors:
            try:
                # First check if element is present
                element = self.wait_for_presence(by, selector)
                if element:
                    # Then check if it's clickable
                    clickable_element = self.wait_for_clickable(by, selector)
                    if clickable_element:
                        return clickable_element
            except:
                continue
        return None

    def find_and_click_group(self, group_name):
        """Find and click a group using improved search"""
        try:
            time.sleep(3)

            # Find search box
            for attempt in range(3):
                search_box = self.find_search_box()
                if search_box:
                    break
                time.sleep(2)

            if not search_box:
                raise NoSuchElementException(
                    "Search box not found after multiple attempts"
                )

            # Clear and focus search box
            self.driver.execute_script("arguments[0].innerHTML = '';", search_box)
            search_box.click()
            time.sleep(1)

            # Type group name
            search_box.send_keys(group_name)
            time.sleep(2)

            # Try different strategies to find the group
            group_xpath_patterns = [
                f"//span[@title='{group_name}']",
                f"//span[contains(@title, '{group_name}')]",
                f"//div[contains(@title, '{group_name}')]",
                f"//div[.//span[contains(text(), '{group_name}')]]",
            ]

            group_element = None
            for xpath in group_xpath_patterns:
                try:
                    group_element = self.wait_for_clickable(By.XPATH, xpath)
                    if group_element:
                        break
                except:
                    continue

            if not group_element:
                raise NoSuchElementException(f"Group '{group_name}' not found")

            # Click the group
            group_element.click()
            time.sleep(2)
            return True

        except Exception as e:
            logging.error(f"Error finding group {group_name}: {str(e)}")
            return False

    def send_message_to_group(self, message):
        """Send a message in the currently open chat"""
        try:
            time.sleep(1)

            message_selectors = [
                (By.CSS_SELECTOR, 'div[title="Type a message"]'),
                (By.XPATH, '//div[@contenteditable="true"][@title="Type a message"]'),
                (By.XPATH, '//div[@role="textbox"][@data-tab="10"]'),
                (By.CSS_SELECTOR, '[data-testid="conversation-compose-box-input"]'),
            ]

            message_box = None
            for by, selector in message_selectors:
                try:
                    message_box = self.wait_for_clickable(by, selector)
                    if message_box:
                        break
                except:
                    continue

            if not message_box:
                raise NoSuchElementException("Message input not found")

            pyperclip.copy(message)
            message_box.click()
            time.sleep(1)
            message_box.send_keys(Keys.CONTROL + "v")
            time.sleep(1)
            message_box.send_keys(Keys.ENTER)
            time.sleep(2)

            return True

        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            return False

    def process_groups(self, groups, message, delay_between_groups=15):
        """Process groups with improved error handling"""
        failed_groups = []

        for group in groups:
            logging.info(f"Processing group: {group}")

            # Try to find and click the group
            for attempt in range(2):
                if self.find_and_click_group(group):
                    break
                time.sleep(2)
            else:
                logging.error(f"Could not find group: {group}")
                failed_groups.append(group)
                continue

            # Try to send the message
            for attempt in range(1):
                if self.send_message_to_group(message):
                    break
                time.sleep(2)
            else:
                logging.error(f"Could not send message to group: {group}")
                failed_groups.append(group)
                continue

            logging.info(f"Successfully sent message to {group}")
            time.sleep(delay_between_groups)

        return failed_groups

    def close(self):
        if hasattr(self, "driver"):
            self.driver.quit()
            logging.info("Browser closed successfully")


def main():
    CHROMEDRIVER_PATH = r"C:\Tools\chromedriver-win64\chromedriver.exe"

    try:
        bot = WhatsAppAutomation(CHROMEDRIVER_PATH)
        login_ui = LoginConfirmation()
        login_ui.create_popup()

        if not login_ui.is_confirmed:
            logging.info("Operation canceled by user")
            return

        groups = [
            "The Fineapples",
            "April birthday",
            "MMARAU comrades",
            "ZETECH TOWN CAMPUS",
        ]

        message_content = """This is a test message sent using the WhatsApp Automation script.
        This message is sent to multiple groups for demonstration purposes.: 
        Thank you for your attention!"""

        failed = bot.process_groups(groups, message_content)

        if failed:
            logging.warning(f"Failed groups: {', '.join(failed)}")
        else:
            logging.info("All messages sent successfully!")

    except Exception as e:
        logging.error(f"Critical error: {str(e)}", exc_info=True)
    finally:
        if "bot" in locals():
            bot.close()


if __name__ == "__main__":
    main()
