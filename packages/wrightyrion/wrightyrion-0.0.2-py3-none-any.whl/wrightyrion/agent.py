import playwright.async_api
from gembox.debug_utils import Debugger
from playwright.async_api import async_playwright, Playwright

from .browser_mgr import SingleBrowserManager
from .page_interactor import PageInteractor
from .data_extractor import DataExtractor


class Agent:
    def __init__(self,
                 wright: Playwright,
                 headless: bool,
                 debug_tool: Debugger):
        """
        Initialize the Agent.

        **Note: Usually, you need to instantiate an agent by Calling `Agent.instantiate()` rather than `Agent()`**

        :param wright:
        :param headless:
        :param debug_tool:
        """
        self._wright = wright
        self._headless = headless
        self._debug_tool = debug_tool
        self._browser_mgr = SingleBrowserManager(wright=wright, headless=headless, debug_tool=debug_tool)
        self._page_interactor = None
        self._data_extractor = None
        self._is_running = False

    async def start(self, **kwargs):
        if self.is_running is True:
            self.debug_tool.warn("Agent is already running. No need to start again")
        else:
            self.debug_tool.info(f"Starting agent...")
            await self.browser_mgr.start(**kwargs)
            self._page_interactor = PageInteractor(page=self.page, debug_tool=self.debug_tool)
            self._data_extractor = DataExtractor(page=self.page, debug_tool=self.debug_tool)
            self._is_running = True
            self.debug_tool.info(f"Agent started successfully")

    async def stop(self):
        if self.is_running is False:
            self.debug_tool.warn("Agent is not running. No need to stop")
        else:
            self.debug_tool.info(f"Stopping agent...")
            await self.browser_mgr.close()
            self._page_interactor = None
            self._data_extractor = None
            self._is_running = False
            self.debug_tool.info(f"Agent stopped successfully")

    @classmethod
    async def instantiate(cls, headless=True, debug_tool=None):
        wright = await (async_playwright().start())
        instance = cls(wright=wright, headless=headless, debug_tool=debug_tool)
        return instance

    @property
    def wright(self):
        """the playwright instance"""
        return self._wright

    @property
    def browser_mgr(self) -> SingleBrowserManager:
        return self._browser_mgr

    @property
    def page_interactor(self) -> PageInteractor:
        return self._page_interactor

    @property
    def data_extractor(self) -> DataExtractor:
        return self._data_extractor

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def page(self) -> playwright.async_api.Page:
        return self.browser_mgr.page

    @property
    def debug_tool(self) -> Debugger:
        return self._debug_tool
