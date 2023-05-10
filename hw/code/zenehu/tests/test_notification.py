from zenehu.pages.notification_page import NotificationPage
from zenehu.tests.base_case import BaseCase


class TestNotifications(BaseCase):
    authorize = True

    # Popup уведомления. Список уведомлений отображается при нажатии на колокольчик
    def test_notification_open(self):
        notification_page = NotificationPage(self.browser)
        notification_page.render(notification_page.url)
        notification_page.open_notifications()
        # assert if notifications list has class sub-menu_enable
        assert notification_page.find(notification_page.Locators.NOTIFICATIONS_LIST).get_attribute(
            'class') == 'sub-menu sub-menu__back bg_sub-menu sub-menu_enable'

    # Popup уведомления. Удаление всех уведомлений
    def test_notification_delete(self):
        notification_page = NotificationPage(self.browser)
        notification_page.render(notification_page.url)

        notification_page.open_notifications()
        notification_page.delete_notifications()
        assert notification_page.check_empty_notifications().text == 'Новых уведомлений нет.'

    # Popup уведомления. Сообщение "нет уведомлений" если список пуст
    def test_notification_empty(self):
        notification_page = NotificationPage(self.browser)
        notification_page.render(notification_page.url)

        notification_page.open_notifications()
        notification_page.delete_notifications()
        assert notification_page.check_empty_notifications().text == 'Новых уведомлений нет.'
