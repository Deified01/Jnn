import asyncio
import logging
import re
import threading
from datetime import datetime
from telethon.sync import TelegramClient
from telethon import events
from telethon.sessions import StringSession
from flask import Flask

# Replace with your Telegram API credentials
api_id = 8447214
api_hash = '9ec5782ddd935f7e2763e5e49a590c0d'
string_session = "1BVtsOHYBu7wVbjA98EfMVYL1qSL4GAiNbRGZSHTwVL7Me71M5E4kv2XqaQJRqUNt8a3-8CL9t9gLHTj4xcytGQI_qG9XFsALxcVh8LqfGSvWGW-enmSnvJcRJc6XpbiJzWFwK5r3_qNRXo72TGMQuZ3HFT89h09jq93Y8G8K4p9MggQ5ty_BPS4BytiPODkpX57Ew_8aUyrFBPGPti9hOmnKqXPv0pk5oRHI-dYNTMlKWjncE7tGoIHo1ggM9DPdwcDqmE0zQomSTLOuL3jUsWwpWV8SpLM-Y2SW5MqKjsZL2K-EvYpWY78tMU3dS8Cu1VhEZus0q1Bl5e-A5kpblNRgMIvZklE="

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask setup
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

# Telethon client setup
client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Main function to run before starting the client
async def main():
    logger.info('''
 ___                   _______            _________________
|   |                /   ___   \         |______    _______|
|   |               /   /   \   \               |   |
|   |              /   /__ __\   \              |   |
|   |    ___      /   ________\   \             |   |
|   |___|   |    /   /         \   \      ______|   |______
\___________/   /___/           \___\    |_________________|
''')

    # Run the riddle and other tasks concurrently
    await asyncio.gather(
        send_riddle(),
        send_propose(),
        send_tesure(),
        send_shunt(),
        send_sfight()
    )

# Task to send /propose every 10 minutes with a 2-second delay
async def send_propose():
    while True:
        try:
            await client.send_message("@lustsupport", "/propose")
            logger.info("Sent /propose")
            await asyncio.sleep(2)  # 2 seconds delay
            await asyncio.sleep(600)  # 10 minutes
        except Exception as e:
            logger.error(f"Error sending /propose: {e}")

# Task to send /tesure every 30 minutes with a 2-second delay
async def send_tesure():
    while True:
        try:
            await client.send_message("@lustsupport", "/tesure")
            logger.info("Sent /tesure")
            await asyncio.sleep(2)  # 2 seconds delay
            await asyncio.sleep(1800)  # 30 minutes
        except Exception as e:
            logger.error(f"Error sending /tesure: {e}")

# Task to send /shunt every 1 minute with a 2-second delay
async def send_shunt():
    while True:
        try:
            await client.send_message("@lustsupport", "/shunt")
            logger.info("Sent /shunt")
            await asyncio.sleep(2)  # 2 seconds delay
            await asyncio.sleep(60)  # 1 minute
        except Exception as e:
            logger.error(f"Error sending /shunt: {e}")

# Task to send /sfight every 10 minutes with a 2-second delay
async def send_sfight():
    while True:
        try:
            await client.send_message("@lustsupport", "/sfight")
            logger.info("Sent /sfight")
            await asyncio.sleep(2)  # 2 seconds delay
            await asyncio.sleep(600)  # 10 minutes
        except Exception as e:
            logger.error(f"Error sending /sfight: {e}")

# Task to send /riddle and handle wait times
async def send_riddle():
    while True:
        try:
            await client.send_message("@lustXcatcherrobot", "/riddle")
            response = await client.get_messages("@lustXcatcherrobot", limit=1)
            response_text = response[0].text
            logger.info(f"Received response: {response_text}")
            if "Please wait" in response_text:
                wait_time_match = re.search(r'Please wait (\d+) seconds', response_text)
                if wait_time_match:
                    wait_time = int(wait_time_match.group(1))
                    if wait_time == 0:
                        logger.info("Wait time is 0, sending immediately...")
                        continue  # Skip the sleep and send immediately
                    else:
                        logger.info(f"Waiting for {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
            else:
                logger.info("Waiting for 10 seconds (default)...")
                await asyncio.sleep(8)  # Default wait time if no specific wait time is found
        except Exception as e:
            logger.error(f"Error sending riddle: {e}")

# Flask app runner
def run_flask_app():
    app.run(host='0.0.0.0', port=10000)

# Main entry point
if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Start Telethon client and run main function
    client.start()
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
