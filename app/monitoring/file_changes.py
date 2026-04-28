import loguru
import watchfiles

from app.core import CONFIG


for changes in watchfiles.watch(CONFIG.MONITORING_FOLDER):
   loguru.logger.info(f"Detected change to: {', '.join(changes)}")