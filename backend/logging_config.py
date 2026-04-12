import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "backend.log"

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=3)
handler.setFormatter(formatter)

logger = logging.getLogger("vehicle_diagnostics_api")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Also print warnings and above to console for local development
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
