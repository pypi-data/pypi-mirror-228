from selenium.webdriver.common.by import By
from typing import Optional
from selenium.webdriver import Edge, Chrome, Firefox, Safari
import logging


class Time_Format:
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    
class YoutubeManagerException(Exception):
    pass

class BaseYoutubeManager:
    def __init__(
        self,
        links_dict: Optional[dict[str | int, str]] = None,
        link: Optional[str] = None,
        driver: Edge | Chrome | Firefox | Safari = Firefox,
        sleep_until_end_video: bool = False
    ) -> None:
        self._links = links_dict
        self._link = link
        self._driver: Edge | Chrome | Firefox | Safari = driver()
        self._logger = logging.getLogger("yt_manager")
        self._sleep_until_end_video = sleep_until_end_video
        self._status: dict[str, bool] = {}
        self._el = {
            "video_time": (By.CLASS_NAME, "ytp-time-duration"),
            "play": (By.CSS_SELECTOR, ".ytp-play-button"),
            "full_screen": (
                By.CSS_SELECTOR,
                "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-right-controls > button.ytp-fullscreen-button.ytp-button",
            ),
        }

    def __get_link(self, key: str | int) -> str:
        if isinstance(key, str) or isinstance(key, int):
            return self._links[key]
        else:
            raise TypeError(f"Must be a string or integer type instead of {type(key)}")
      
    def __time_translation(self, yt_time: str, decimal_places: int):
        if yt_time.count(":") == 1:
            hours, minutes, seconds = map(int, [0] + yt_time.split(":") )
        elif yt_time.count(":") == 2:
            hours, minutes, seconds = map(int, yt_time.split(":"))
        
        return {
            "seconds" : float(seconds + minutes * 60 + hours * 3600),
            "minutes": round(float(seconds / 60 + minutes  + hours * 60), decimal_places),
            "hours": round(float(seconds / 3600 + minutes / 60  + hours), decimal_places)
        }
    
    def __call__(self) -> dict:
        return self.__dict__
     
    def __str__(self) -> str:
        return f"Class {self.__class__.__name__}"
