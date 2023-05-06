import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()