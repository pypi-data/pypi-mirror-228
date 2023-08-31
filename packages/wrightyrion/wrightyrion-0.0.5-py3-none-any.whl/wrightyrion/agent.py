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
        assert isinstance(wright, Playwright), f"wright should be a Playwright instance, but got {wright.__class__.__name__}"
        assert isinstance(debug_tool, Debugger), f"debug_tool should be a Debugger instance, but got {debug_tool.__class__.__name__}"

        self._wright = wright
        self._headless = headless
        self._debug_tool = debug_tool
        self._browser_mgr = SingleBrowserManager(wright=wright, headless=headless, debug_tool=debug_tool)
        self._page_interactor = None
        self._data_extractor = None
        self._is_running = False

        # init hook
        self._init_hook()

    @classmethod
    async def instantiate(cls, headless=True, debug_tool=None) -> 'Agent':
        """
        Instantiate an agent.

        :param headless: (bool) whether the browser is headless
        :param debug_tool: (Debugger) the debugger
        :return: (Agent) the agent instance
        """
        wright = await (async_playwright().start())
        debug_tool = Debugger() if debug_tool is None else debug_tool
        instance = cls(wright=wright, headless=headless, debug_tool=debug_tool)
        return instance

    async def start(self, **kwargs):
        if self.is_running:
            self.debug_tool.warn(f"{self.__class__.__name__} is already running. No need to start again")
        else:
            self.debug_tool.info(f"Starting {self.__class__.__name__}...")
            await self.browser_mgr.start(**kwargs)
            self._page_interactor = PageInteractor(page=self.page, debug_tool=self.debug_tool)
            self._data_extractor = DataExtractor(page=self.page, debug_tool=self.debug_tool)
            # start hook
            await self._start_hook()
            self._is_running = True
            self.debug_tool.info(f"{self.__class__.__name__} started successfully")

    async def stop(self):
        if self.is_running is False:
            self.debug_tool.warn("Agent is not running. No need to stop")
        else:
            self.debug_tool.info(f"Stopping agent...")
            await self.browser_mgr.close()
            self._page_interactor = None
            self._data_extractor = None
            # stop hook
            await self._stop_hook()
            self._is_running = False
            self.debug_tool.info(f"Agent stopped successfully")

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

    # hooks
    def _init_hook(self) -> None:
        """
        Hook function called at the end of the __init__ functions.

        When calling this hook, the agent already has `self.wright`, `self.debug_tool` and `self.browser_mgr` equipped.
        :return: (None)
        """
        pass

    async def _start_hook(self) -> None:
        """
        Hook function called after the agent is started, just before setting self._is_running to True.

        After starting the agent, the agent now have the browser instance and a blank page instance.
        :return: (None)
        """
        pass

    async def _stop_hook(self) -> None:
        """
        Hook function called after the agent is stopped, just before setting self._is_running to False.

        After stopping the agent, the agent now have no browser instance and no page instance.
        :return: (None)
        """
        pass
