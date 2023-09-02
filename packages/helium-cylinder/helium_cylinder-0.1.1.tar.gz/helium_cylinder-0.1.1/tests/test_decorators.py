from unittest import TestCase
from unittest.mock import MagicMock, patch

from selenium.webdriver import ChromeOptions, FirefoxOptions

from helium_cylinder import decorators as d


@patch("helium_cylinder.decorators.start_firefox")
class UsingFirefoxTestCase(TestCase):
    def test_without_parenthesis(self, start_firefox):
        @d.using_firefox
        def f():
            ...

        f()

        start_firefox.assert_called_once_with(options=None, headless=False)

    def test_with_parenthesis(self, start_firefox):
        @d.using_firefox()
        def f():
            ...

        f()

        start_firefox.assert_called_once_with(options=None, headless=False)

    def test_with_options(self, start_firefox):
        options = MagicMock(spec=FirefoxOptions)

        @d.using_firefox(options=options)
        def f():
            ...

        f()

        start_firefox.assert_called_once_with(options=options, headless=False)

    def test_headless(self, start_firefox):
        @d.using_firefox(headless=True)
        def f():
            ...

        f()

        start_firefox.assert_called_once_with(options=None, headless=True)

    def test_headless_with_options(self, start_firefox):
        options = MagicMock(spec=FirefoxOptions)

        @d.using_firefox(options=options, headless=True)
        def f():
            ...

        f()

        start_firefox.assert_called_once_with(options=options, headless=True)


@patch("helium_cylinder.decorators.start_chrome")
@patch("helium_cylinder.decorators.chromedriver_autoinstaller")
class UsingChromeTestCase(TestCase):
    def test_without_parenthesis(
        self, chromedriver_autoinstaller, start_chrome
    ):
        @d.using_chrome
        def f():
            ...

        f()

        chromedriver_autoinstaller.install.assert_called_once_with()
        start_chrome.assert_called_once_with(options=None, headless=False)

    def test_with_parenthesis(self, chromedriver_autoinstaller, start_chrome):
        @d.using_chrome()
        def f():
            ...

        f()

        chromedriver_autoinstaller.install.assert_called_once_with()
        start_chrome.assert_called_once_with(options=None, headless=False)

    def test_with_options(self, chromedriver_autoinstaller, start_chrome):
        options = MagicMock(spec=ChromeOptions)

        @d.using_chrome(options=options)
        def f():
            ...

        f()

        chromedriver_autoinstaller.install.assert_called_once_with()
        start_chrome.assert_called_once_with(options=options, headless=False)

    def test_headless(self, chromedriver_autoinstaller, start_chrome):
        @d.using_chrome(headless=True)
        def f():
            ...

        f()

        chromedriver_autoinstaller.install.assert_called_once_with()
        start_chrome.assert_called_once_with(options=None, headless=True)

    def test_headless_with_options(
        self, chromedriver_autoinstaller, start_chrome
    ):
        options = MagicMock(spec=ChromeOptions)

        @d.using_chrome(options=options, headless=True)
        def f():
            ...

        f()

        chromedriver_autoinstaller.install.assert_called_once_with()
        start_chrome.assert_called_once_with(options=options, headless=True)
