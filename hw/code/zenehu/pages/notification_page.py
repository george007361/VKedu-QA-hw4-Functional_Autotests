from selenium.webdriver.common.by import By

from zenehu.pages.feed_page import FeedPage


class NotificationPage(FeedPage):
    class Locators:
        NOTIFICATION_BTN = (
            By.XPATH, '//div[@class="notice-bell"]'
        )
        NOTIFICATIONS = (
            By.XPATH,
            '//span[@class="back-notice-container__notice font_regular"]'
        )
        NOTIFICATIONS_DELETE = (
            By.XPATH,
            '//span[text()="Удалить все"]/parent::button'
        )
        NOTIFICATIONS_EMPTY_SPAN = (
            By.XPATH,
            '//span[text()="Новых уведомлений нет."]'
        )
        NOTIFICATIONS_LIST = (
            By.XPATH,
            '//div[@class="back-notice-container"]/parent::div[contains(@class, "sub-menu sub-menu__back bg_sub-menu")]'
        )
        SUBSCRIBE_BUTTON = (
            By.XPATH,
            '//span[text()="Подписаться"]/parent::button'
        )
        UNSUBSCRIBE_BUTTON = (
            By.XPATH,
            '//span[text()="Отписаться"]/parent::button'
        )

    def open_notifications(self):
        self.click(self.Locators.NOTIFICATION_BTN)

    def delete_notifications(self):
        button = self.find(self.Locators.NOTIFICATIONS_DELETE)
        if 'profile-container__erase-btn_hide' not in button.get_attribute('class'):
            self.click(button)

    def check_empty_notifications(self):
        return self.find(self.Locators.NOTIFICATIONS_EMPTY_SPAN)
