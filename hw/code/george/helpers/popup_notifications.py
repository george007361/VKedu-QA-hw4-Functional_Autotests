from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class PopupNotification:
    class Locator:
        def NOTIF_ERROR(text):
            return (By.XPATH, f'//span[starts-with(@class, "notice__msg") and starts-with(text(), "{text}")]')

    def exists(page: BasePage, content):
        print(PopupNotification.Locator.NOTIF_ERROR(content))
        page.find(PopupNotification.Locator.NOTIF_ERROR(content))
