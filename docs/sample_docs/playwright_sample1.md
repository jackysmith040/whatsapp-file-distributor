```python
import asyncio
from playwright.async_api import async_playwright
import csv
from datetime import datetime
import random

# WhatsApp Web URL
WHATSAPP_WEB = "https://web.whatsapp.com/"

# Message components
HELLO = "Hi "  # Greeting to start the message
MEET_AND_GREET = ", hope I find you well\n\n"  # Contextual intro
BODY = "(whatever message you want to send)"  # Main message body

# String to search in previous messages to avoid duplicates
CHECK_STRING = "STRING TO SEARCH"

# Input file containing leads (CSV format)
FILE_TO_OPEN = "leads.csv"

# Dictionary to track statistics during execution
stats = {
    "sent": 0,  # Number of successfully sent messages
    "failed": 0,  # Number of failed message attempts
    "without_whatsapp": [],  # Leads without WhatsApp
    "existent_chat": []  # Leads who already received the message
}

# Logs a message with a timestamp
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
    print(f"[{timestamp}] {message}")  # Print the formatted log message

# Formats a name by removing unnecessary characters and capitalizing it
def name_formatter(name_and_surname):
    try:
        # Extract the first "word" from the name (ignores additional parts)
        name = name_and_surname.split()[0]
        # Replace underscores, convert to lowercase, and capitalize
        return name.replace("_", " ").lower().title()
    except IndexError:
        # If the name is empty or malformed, return it as is
        return name_and_surname

# Sends a message to a specified phone number using WhatsApp Web
async def send_message(page, number, message, name, full_name):
    try:
        # Step 1: Search for the number in WhatsApp search box
        await page.fill('div[data-testid="chat-list-search"]', number)
        await page.wait_for_timeout(2000)  # Wait for results to load

        # Step 2: Check if the contact exists and click to open chat
        contact = await page.locator('div[data-testid="cell-frame-container"]').first()
        await contact.click()

        # Step 3: Check if the message has already been sent
        elementi_messaggi = await page.locator(f'text="{CHECK_STRING}"').count()
        if elementi_messaggi > 0:
            log(f"{name} already received the message.")  # Log and return
            stats["existent_chat"].append((name, number))  # Add to stats
            return False

        # Step 4: Locate the message input field
        message_field = await page.locator('div[title="Write message"]').first()
        if not message_field:
            # Raise an error if the input field is not found (e.g., blocked contact)
            raise Exception("Message field not found, possibly blocked.")

        # Step 5: Type the message and press Enter to send
        await message_field.type(message)  # Enter the full message
        await message_field.press("Enter")  # Send the message
        log(f"Successfully sent message to {full_name}.")  # Log success
        stats["sent"] += 1  # Update success stats
        return True
    except Exception as e:
        # Handle any exceptions during message sending
        log(f"Error sending message to {full_name}: {e}")
        stats["failed"] += 1  # Update failure stats
        return False

# Main function to orchestrate message sending
async def main():
    # Initialize Playwright and launch the browser in persistent mode
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="/home/dario/.config/google-chrome",  # Use existing login session
            headless=False  # Run browser in visible mode for debugging
        )
        page = await browser.new_page()  # Create a new page (tab)
        await page.goto(WHATSAPP_WEB)  # Open WhatsApp Web

        # Wait for the user to scan the QR Code
        log("Scan WhatsApp Web QR Code to continue...")
        await page.wait_for_selector('div[data-testid="chat-list-search"]')  # Ensure successful login
        log("QR Code successfully scanned!")  # Log success

        # Open the leads CSV file
        with open(FILE_TO_OPEN, newline='') as csvfile:
            reader = csv.reader(csvfile)  # Read the CSV file
            contacts = [row for row in reader]  # Convert rows to a list
        
        # Iterate over the contacts and send messages
        for lead in contacts:
            try:
                # Extract name and number from the current lead
                name = name_formatter(lead[0])  # Format the name
                number = lead[1]  # Extract the phone number

                # Compose the full message
                message = HELLO + name + MEET_AND_GREET + BODY

                # Send the message and add a random delay
                await send_message(page, number, message, name, lead[0])
                await asyncio.sleep(random.uniform(1, 2))  # Delay to reduce bot detection risk
            except IndexError:
                # Handle malformed rows (e.g., missing columns)
                log(f"Skipping malformed row: {lead}")
                continue

        # Log final statistics
        log(f"Successfully sent {stats['sent']} messages")
        log(f"Failed to send {stats['failed']} messages")

        # Close the browser session
        await browser.close()

# Entry point of the script
if __name__ == "__main__":
    # Run the main function in the asyncio event loop
    asyncio.run(main())