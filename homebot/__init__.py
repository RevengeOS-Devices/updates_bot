__version__ = "1.0.0"

from dotenv import load_dotenv
import os
from pathlib import Path
from telegram.ext import Updater

bot_path = Path(__file__).parent
get_config = os.environ.get

load_dotenv("config.env")

updater = Updater(token=get_config("BOT_API_TOKEN"), use_context=True)
dispatcher = updater.dispatcher
