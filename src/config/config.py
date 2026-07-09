import logging
from dotenv import load_dotenv
from utils.utils import get_env

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log", mode='a', delay=False, encoding='utf-8'), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

API_ID = int(get_env("API_ID"))
API_HASH = get_env("API_HASH")
TOKEN = get_env("BOT_TOKEN")