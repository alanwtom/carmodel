import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Set up a rotating file handler (log rotation)
    handler = RotatingFileHandler('app.log', maxBytes=5*1024*1024, backupCount=3)
    handler.setLevel(logging.DEBUG)  # Log all levels from DEBUG upwards

    # Define log message format (timestamp, log level, message)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handler to the root logger
    logging.getLogger().addHandler(handler)

    # Set logging level to capture all messages
    logging.basicConfig(level=logging.DEBUG)

    # Also log to the console (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Log level for console (INFO and above)
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    # Now you can use logging in your app
    logging.info("Logging setup complete")