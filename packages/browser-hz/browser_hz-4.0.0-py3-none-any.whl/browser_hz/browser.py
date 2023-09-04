import re
from contextlib import contextmanager
from logging import Logger, getLogger
from typing import Tuple, Generator

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire.inspect import InspectRequestsMixin
from seleniumwire.request import Request

LOGGER: Logger = getLogger(__name__)


class Browser:

    def __init__(self, driver: WebDriver | InspectRequestsMixin):
        self.driver: WebDriver | InspectRequestsMixin = driver

    def open_page(self, url: str) -> 'Browser':
        LOGGER.info(f'Open page [{url}]')
        self.driver.get(url)
        return self

    def click(self, locator: Tuple[str, str]) -> 'Browser':
        LOGGER.info(f'Click element with locator [{locator}]')
        self.__wait_for_element_to_be_clickable(locator)
        element_to_be_clicked: WebElement = self.driver.find_element(by=locator[0], value=locator[1])
        element_to_be_clicked.click()
        return self

    @contextmanager
    def click_with_redirect_to_new_tab(self, locator: Tuple[str, str]) -> Generator['Browser', None, None]:
        try:
            yield self.click(locator)
        finally:
            self.close_newly_opened_tab()

    def get_network_traffic(self, requests_paths_to_wait: list[str], timeout: int = 1) -> list[Request]:
        requests: list[Request] = []
        for request_path_to_wait in requests_paths_to_wait:
            try:
                requests.append(self.driver.wait_for_request(pat=re.escape(request_path_to_wait), timeout=timeout))
            except TimeoutException:
                requests.append(self.__get_unsuccessfully_processed_request(request_path_to_wait))
        return requests

    def close_tab(self) -> 'Browser':
        LOGGER.info('Close tab')
        self.driver.close()
        return self

    def close_browser(self) -> 'Browser':
        LOGGER.info('Close web browser_hz')
        self.driver.quit()
        return self

    def close_newly_opened_tab(self) -> 'Browser':
        window_handles: list[str] = self.driver.window_handles
        if len(window_handles) == 2:
            self.driver.switch_to.window(window_handles[1])
            self.close_tab()
            self.driver.switch_to.window(window_handles[0])
        return self

    def __wait_for_element_to_be_clickable(self, locator: Tuple[str, str]) -> 'Browser':
        wait: WebDriverWait = WebDriverWait(self.driver, timeout=5)
        wait.until(expected_conditions.element_to_be_clickable(locator))
        return self

    def __get_unsuccessfully_processed_request(self, request_path_to_wait: str) -> Request:
        if request := [request for request in self.driver.requests if request_path_to_wait in request.url]:
            return request[0]
        raise NoSuchElementException(f'Request with path matching {request_path_to_wait} has not been sent')
