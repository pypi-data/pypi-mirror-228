import pathlib
from typing import Union, List

import playwright
from gembox.debug_utils import Debugger


class PageInteractor:
    def __init__(self, page, debug_tool: Debugger = None):
        self._page: playwright.async_api.Page = page
        self._debug_tool = Debugger() if debug_tool is None else debug_tool

    @property
    def page(self) -> Union[None, playwright.async_api.Page]:
        return self._page

    @property
    def debug_tool(self) -> Debugger:
        return self._debug_tool

    async def get_element(self, selector: str, strict: bool = False) -> playwright.async_api.ElementHandle:
        """
        Get the element according to the selector.

        If `strict` is True, then when resolving multiple elements, the function will raise Error
        """
        return await self.page.query_selector(selector=selector, strict=strict)

    async def get_elements(self, selector: str) -> List[playwright.async_api.ElementHandle]:
        """
        Get the elements according to the selector.

        :param selector: (str) the selector
        :return: (List[playwright.async_api.ElementHandle]) the elements
        """
        return await self.page.query_selector_all(selector=selector)

    async def click(self, selector: str):
        return await self.page.click(selector=selector)

    async def type_input(self, selector: str, text: str):
        return await self.page.type(selector=selector, text=text)

    async def download_page(self, file_path: (str, pathlib.Path), encoding="utf-8"):
        """
        Download the current web page.

        :param file_path: (str, pathlib.Path) the file path
        :param encoding: (str, optional) the encoding of the file, default is utf-8
        :return: (None)
        """
        self.debug_tool.info(f"Downloading the webpage, page url: {self.page.url}...")
        content = await self._page.content()
        self.debug_tool.info(f"Pumping the content to {file_path}...")
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        self.debug_tool.info(f"Downloaded the webpage successfully, page url: {self.page.url}, file_path: {file_path}")

