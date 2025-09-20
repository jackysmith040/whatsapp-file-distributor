```python
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event

# Initialize client
client = NewClient("your_bot_name")

@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print("🎉 Bot connected successfully!")

@client.event  
def on_message(client: NewClient, event: MessageEv):
    if event.message.conversation == "hi":
        client.reply_message("Hello! 👋", event.message)

# Start the bot
client.connect()
event.wait()  # Keep running


# Async Version

import asyncio
from neonize.aioze.client import NewAClient
from neonize.aioze.events import MessageEv, ConnectedEv

async def main():
    client = NewAClient("async_bot")
    
    @client.event
    async def on_message(client: NewAClient, event: MessageEv):
        if event.message.conversation == "ping":
            await client.reply_message("pong! 🏓", event.message)
    
    await client.connect()

asyncio.run(main())


# Basic Client Setup

from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

# Initialize the WhatsApp client
client = NewClient(
    name="my-whatsapp-bot",
    database="./neonize.db"
)

# Handle successful connection
@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print("🎉 Successfully connected to WhatsApp!")
    print(f"📱 Device: {event.device}")

# Start the client
client.connect()
event.wait()

# Sedning messages

from neonize.utils import build_jid

# Send simple text message
jid = build_jid("1234567890")
client.send_message(jid, text="Hello from Neonize! 🚀")

# Send image with caption
with open("image.jpg", "rb") as f:
    image_data = f.read()

image_msg = client.build_image_message(
    image_data,
    caption="Check out this amazing image! 📸",
    mime_type="image/jpeg"
)
client.send_message(jid, message=image_msg)

# Send document file
with open("document.pdf", "rb") as f:
    doc_data = f.read()

doc_msg = client.build_document_message(
    doc_data,
    filename="document.pdf",
    caption="Here is the document you requested",
    mime_type="application/pdf"
)
client.send_message(jid, message=doc_msg)



# message event handling

from neonize.events import MessageEv, ReceiptEv, PresenceEv
from datetime import datetime

# Handle incoming text messages
@client.event
def on_message(client: NewClient, event: MessageEv):
    message_text = event.message.conversation
    sender_jid = event.info.message_source.sender
    chat_jid = event.info.message_source.chat
    
    print(f"📨 Received from {sender_jid}: {message_text}")
    
    # Auto-reply functionality
    if message_text and message_text.lower() == "hello":
        client.send_message(chat_jid, text="Hello there! 👋")
    elif message_text and message_text.lower() == "help":
        help_text = """
🤖 *Bot Commands:*
• hello - Get a greeting
• help - Show this help message
• time - Get current time
• joke - Get a random joke
"""
        client.send_message(chat_jid, text=help_text)
    elif message_text and message_text.lower() == "time":
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client.send_message(chat_jid, text=f"🕐 Current time: {current_time}")

# Handle message receipts (delivery status)
@client.event
def on_receipt(client: NewClient, event: ReceiptEv):
    print(f"📧 Message {event.receipt.type}: {event.message_ids}")

# Handle typing indicators
@client.event
def on_presence(client: NewClient, event: PresenceEv):
    chat = event.message_source.chat
    participant = event.message_source.sender
    print(f"💬 {participant} is {event.presence} in {chat}")


# Group management

from neonize.utils import build_jid

# Create a new group
participants = [
    build_jid("1234567890"),
    build_jid("0987654321"),
]

group_info = client.create_group(
    "My Awesome Group 🚀",
    participants
)
print(f"🎉 Group created: {group_info.jid}")

# Get group information
group_info = client.get_group_info(group_jid)
print(f"📋 Group Name: {group_info.group_name}")
print(f"📝 Description: {group_info.group_desc}")
print(f"👥 Participants: {len(group_info.participants)}")

# Add participants to group
client.update_group_participants(
    group_jid,
    [user_jid],
    "add"
)

# Remove participants from group
client.update_group_participants(
    group_jid,
    [user_jid],
    "remove"
)

# Update group name
client.update_group_name(
    group_jid,
    "New Group Name 🎯"
)

# Update group description
client.update_group_description(
    group_jid,
    "This is our updated group description"
)


# Contact and Profile management

# Get user profile information
profile = client.get_profile_picture(
    user_jid,
    full_resolution=True
)
print(f"👤 Profile picture URL: {profile.url}")
print(f"🆔 Profile ID: {profile.id}")

# Update your own status
client.set_presence("available")
print("✅ Status updated to available")

# Check if contacts are on WhatsApp
contacts = ["1234567890", "0987654321", "1122334455"]
registered_contacts = client.is_on_whatsapp(contacts)

for contact in registered_contacts:
    if contact.is_in:
        print(f"✅ {contact.jid} is on WhatsApp")
    else:
        print(f"❌ {contact.query} is not on WhatsApp")


        

