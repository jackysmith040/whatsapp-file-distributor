import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- Candidate Selectors to Test ---
# We will test each of these to see which one works reliably on your system.
SELECTORS_TO_TEST = {
    "pane_side": ('css', "div[data-testid='pane-side']"),
    "search_box_testid": ('xpath', '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p'),
    "search_box_title": ('css', 'div[title="Search or start new chat"]'),
    "search_box_xpath": ('xpath', '//div[@contenteditable="true"][@title="Search or start new chat"]'),
}

def run_diagnostic():
    """Launches browser and tests a list of selectors."""
    driver = None
    try:
        print("--- Starting Selector Diagnostic Tool ---")
        options = webdriver.ChromeOptions()
        # NOTE: Using a temporary directory to ensure a clean session for testing.
        # You may be asked to scan the QR code.
        options.add_argument("--start-maximized")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 20) # 20 second wait time

        driver.get("https://web.whatsapp.com")

        print("\n" + "="*50)
        print("--- ACTION REQUIRED ---")
        print("Please log in to WhatsApp Web. Scan the QR code if needed.")
        input("===> Once your chat list is fully visible, press Enter in this terminal...")
        print("✅ User confirmed login. Running diagnostics...")
        time.sleep(3) # Give page time to settle

        
        print("\n--- Testing Selectors ---")
        results = {}
        for key, (by_str, selector) in SELECTORS_TO_TEST.items():
            print(f"Testing selector for '{key}'...")
            try:
                by = getattr(By, by_str.upper() + '_SELECTOR' if by_str == 'css' else by_str.upper())
                wait.until(EC.presence_of_element_located((by, selector)))
                results[key] = "✅ SUCCESS: Element was found."
                print(results[key])
            except TimeoutException:
                results[key] = "❌ FAILED: Element could not be found."
                print(results[key])
            except Exception as e:
                results[key] = f"❌ FAILED with unexpected error: {e}"
                print(results[key])

        print("\n--- Diagnostic Complete ---")
        print("Please copy and paste this entire report back to me:")
        print("\n" + "="*20 + " REPORT " + "="*20)
        for key, result in results.items():
            print(f"{key}: {result}")
        print("="*48)

    except Exception as e:
        print(f"\nA critical error occurred: {e}")
    finally:
        if driver:
            print("\nClosing browser.")
            driver.quit()

if __name__ == "__main__":
    run_diagnostic()