from selenium.webdriver.common.by import By
from yt_manager.core import BaseYoutubeManager, YoutubeManagerException, Time_Format
from typing import Optional
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Edge, Chrome, Firefox, Safari
from time import sleep


class SyncYoutubeManager(BaseYoutubeManager):
    def __init__(
        self,
        links_dict: Optional[dict[str | int, str]] = None,
        link: Optional[str] = None,
        driver: Edge | Chrome | Firefox | Safari = Firefox,
        sleep_until_end_video: bool = False
    ) -> None:
        super().__init__(links_dict, link, driver, sleep_until_end_video)

    def __found_buttons(self) -> dict:
        wait = WebDriverWait(self._driver, 5)
        play = wait.until(EC.presence_of_element_located(self._el["play"]))
        full_screen = wait.until(
            EC.presence_of_element_located(self._el["full_screen"])
        )
        return {"play": play, "full_screen": full_screen}
    
    def __get_video_time(self, format: str =  Time_Format.SECONDS, decimal_places: int = 4) -> str:
        if format in (Time_Format.SECONDS, Time_Format.MINUTES, Time_Format.HOURS):
            wait = WebDriverWait(self._driver, 5)
            video_duration_element = wait.until(
                EC.presence_of_element_located(self._el["video_time"])
            )
            return self._BaseYoutubeManager__time_translation(video_duration_element.text, decimal_places)[format]
        else:
            raise YoutubeManagerException("Wrong time format!")
    

    def open_link(
        self, key: Optional[str], link: Optional[str] = None, timeout: float | int = 2.5
    ) -> None:
        if bool(self._link):
            self._driver.get(self._link)

        elif bool(self._links):
            self._driver.get(self._BaseYoutubeManager__get_link(key))

        else:
            self._driver.get(link)

        self.__buttons = self.__found_buttons()
        self.__video_time = self.__get_video_time()
        sleep(timeout)

    def save_screenshot(self, filename: str = "screenshot.png") -> None:
        if filename.endswith(".png"):
            scr = self._driver.save_screenshot(filename)
            if scr:
                self._logger.debug("Screenshot saved successfully")
            else:
                self._logger.warning("Error while save screenshot")
        else:
            raise ValueError("File name must be with .png extension ")
        
    def get_video_time(self):
        return self.__video_time

    def start(self) -> None:
        if "play" not in self._status.keys() or self._status['play'] != True:
            self.__buttons["play"].click()
            self._status["play"] = True
        
        else:
            raise YoutubeManagerException("Can`t start video which playing")

    def stop(self) -> None:
        if self._status["play"]:
            self.__buttons["play"].click()
            self.status["play"] = False

        else:
            raise YoutubeManagerException("Can`t stop video which not playing")

    def full_screen(self) -> None:
        if "full_screen" not in self._status.keys() or self._status["full_screen"] != True: 
            self.__buttons["full_screen"].click()
            self._status["full_screen"] = True
            self._driver.find_element
            
        else:
            raise YoutubeManagerException("Can`t start video which playing")

    def exit_full_screen(self) -> None:
        if "full_screen" in self._status.keys(): 
            self.__buttons["full_screen"].click()
            self._status["full_screen"] = True
        
        elif "full_screen" not in self._status.keys():
            raise YoutubeManagerException("It is impossible to open a video not in full screen mode when it is not in it")

        else:
            raise YoutubeManagerException("Can`t start video which playing")
        
    def get_cookies(self) -> list[dict]:
        return self._driver.get_cookies()

    def quit(self) -> None:
        self._driver.quit()
