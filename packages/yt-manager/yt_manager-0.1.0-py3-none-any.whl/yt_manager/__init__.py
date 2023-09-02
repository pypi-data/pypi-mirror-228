from yt_manager.core_sync import SyncYoutubeManager
# from yt_manager.core_async import AsyncYoutubeManager
import logging
from yt_manager.core import YoutubeManagerException

logging.basicConfig(
    level=0,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)

Manager = SyncYoutubeManager
# AsyncManager = AsyncYoutubeManager

__all__ = ["Manager", "SyncYoutubeManager", "YoutubeManagerException"]
