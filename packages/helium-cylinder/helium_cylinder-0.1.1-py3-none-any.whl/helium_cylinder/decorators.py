from functools import wraps

import chromedriver_autoinstaller
from helium import start_chrome, start_firefox


def using_firefox(func=None, /, *, options=None, headless=False):
    """Firefoxを使うことを示すデコレータ
    Firefoxを空のページで立ち上げる
    注意：他のデコレータと一緒に使う場合、一番外側に置く必要がある（まずブラウザを立ち上げるため）
    """

    def middle(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_firefox(options=options, headless=headless)
            func(*args, **kwargs)

        return wrapper

    if func is None:
        return middle

    return middle(func)


def using_chrome(func=None, /, *, options=None, headless=False):
    """Google Chromeを使うことを示すデコレータ
    Chromeを空のページで立ち上げる
    注意：他のデコレータと一緒に使う場合、一番外側に置く必要がある（まずブラウザを立ち上げるため）
    """

    def middle(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            chromedriver_autoinstaller.install()
            start_chrome(options=options, headless=headless)
            func(*args, **kwargs)

        return wrapper

    if func is None:
        return middle

    return middle(func)
