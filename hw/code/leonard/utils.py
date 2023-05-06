from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def GetDriver(aBrowserName):
    if aBrowserName == 'chrome':
        options = webdriver.ChromeOptions()
        options.set_capability('browserName', 'chrome')
        options.set_capability('browserVersion', '112.0')
    elif aBrowserName == 'firefox':
        options = webdriver.FirefoxOptions()
        options.set_capability('browserName', 'firefox')
        options.set_capability('browserVersion', '112.0')
    else:
        raise RuntimeError(f'Unsupported browser: "{aBrowserName}"')

    driver = webdriver.Remote(
        'http://127.0.0.1:4444/wd/hub',
        options=options
    )
    driver.maximize_window()
    return driver
