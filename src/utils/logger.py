import logging

def setup_logging():
    """Sets up logging to a file for the application run."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("whatsapp_distributor.log"),
        ]
    )