import logging
import os
from logtail import LogtailHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Logtail handler
logtail_token = os.environ.get("LOGTAIL_TOKEN")
if logtail_token:
    handler = LogtailHandler(source_token=logtail_token)
    logger.addHandler(handler)
else:
    # fallback to console if no Logtail token
    handler = logging.StreamHandler()
    logger.addHandler(handler)

# Optional formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)