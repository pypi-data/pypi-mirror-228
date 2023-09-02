import os

from hashboard.utils.cli import getenv_bool
from hashboard.utils.env import env_with_fallback


HB_DEBUG = getenv_bool("HB_DEBUG")
DEFAULT_CREDENTIALS_FILEPATH = "~/.hashboard/hb_access_key.json"
HB_BASE_URI = env_with_fallback("HB_CLI_BASE_URI", "GLEAN_CLI_BASE_URI", "https://hashboard.com")
FILE_SIZE_LIMIT_MB = 50
