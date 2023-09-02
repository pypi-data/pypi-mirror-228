# This Core in develop!!!
from typing import Optional
from selenium.webdriver import Edge, Chrome, Firefox, Safari
from yt_manager.core import YoutubeManagerException, BaseYoutubeManager


class AsyncYoutubeManager(BaseYoutubeManager):
    def __init__(
        self,
        links_dict: Optional[dict[str | int, str]] = None,
        link: Optional[str] = None,
        driver: Edge | Chrome | Firefox | Safari = Firefox,
        sleep_until_end_video: bool = False
    ) -> None:
        super().__init__(links_dict, link, driver, sleep_until_end_video)
