import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from milchenko.tests.base_case import BaseCase
from milchenko.pages.profile_page import ProfilePage
from milchenko.pages.login_page import LoginPage

def make_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1920, 1080)
    driver.get('https://vdonate.ml')
    return driver

class TestLikes(BaseCase):
    authorize = True

    # Лайки к постам. Нажатие на кнопку лайка серого цвета мгновенно увеличивает суммарное число на единицу
    def test_click_like(self):
      profile_page = ProfilePage(self.browser)
      profile_page.open()
      profile_page.create_post(profile_page)
      profile_page.click_like_button()
      assert '1' == profile_page.find(profile_page.Locators.ACTIVE_LIKE_BUTTON).text
      profile_page.delete_post()

    # Лайки к постам. Нажатие кнопки лайка уменьшает суммарное число на единицу
    def test_click_unlike(self):
      profile_page = ProfilePage(self.browser)
      profile_page.open()
      profile_page.create_post(profile_page)
      profile_page.click_like_button()
      assert '1' == profile_page.find(profile_page.Locators.ACTIVE_LIKE_BUTTON).text
      profile_page.click_unlike_button()
      assert '0' == profile_page.find(profile_page.Locators.LIKE_BUTTON).text
      profile_page.delete_post()

    # Лайки к постам. На каждый лайк автору приходит уведомление: "Пользователь @имя_пользователя оценил ваш пост"
    def test_notify_author_like(self):
       first_driver = self.browser
       second_driver = make_driver()
       
       profile_page = ProfilePage(first_driver)
       profile_page.open()
       profile_page.create_post(profile_page)

       url = profile_page.url

       login_page_2 = LoginPage(second_driver)
       login_page_2.login(os.getenv('IVAN_USERNAME_2'), os.getenv('IVAN_PASSWORD_2'))

       second_driver.get(url)       

       liker = ProfilePage(second_driver)
       liker.click_like_button()

       first_driver.refresh()

       profile_page.click(profile_page.Locators.NOTICE_BELL)
       notification = profile_page.find(profile_page.Locators.NOTIFICATION_FIELD)

       assert notification.text == 'Пользователь ' + os.getenv('IVAN_USERNAME_2') + '\nоценил ваш пост.'

       profile_page.delete_post()
       profile_page.delete_notifications()
       second_driver.quit()

    # Лайки к постам. На каждый отмененный "лайк" уведомление автору не приходит;
    def test_no_notification_unlike(self):
        first_driver = self.browser
        second_driver = make_driver()
       
        profile_page = ProfilePage(first_driver)
        profile_page.open()
        profile_page.create_post(profile_page)

        url = profile_page.url

        login_page_2 = LoginPage(second_driver)
        login_page_2.login(os.getenv('IVAN_USERNAME_2'), os.getenv('IVAN_PASSWORD_2'))

        second_driver.get(url)       

        liker = ProfilePage(second_driver)
        liker.click_like_button()

        first_driver.refresh()

        profile_page.click(profile_page.Locators.NOTICE_BELL)
        profile_page.wait().until(EC.presence_of_element_located(profile_page.Locators.NOTIFICATION_FIELD))

        notification = profile_page.find(profile_page.Locators.NOTIFICATION_FIELD)

        assert notification.text == 'Пользователь ' + os.getenv('IVAN_USERNAME_2') + '\nоценил ваш пост.'

        profile_page.click(profile_page.Locators.NOTICE_BELL)
        profile_page.wait().until(EC.presence_of_element_located(profile_page.Locators.NOTIFICATION_FIELD))
        profile_page.delete_notifications()

        profile_page.wait(20).until_not(EC.presence_of_element_located(profile_page.Locators.FIRST_POPUP))

        profile_page.wait().until(EC.presence_of_element_located(profile_page.Locators.NOTIFICATIONS_EMPTY_SPAN))
        
        liker.click_unlike_button()

        first_driver.refresh()
        profile_page.click(profile_page.Locators.NOTICE_BELL)

        profile_page.wait().until(EC.presence_of_element_located(profile_page.Locators.NOTIFICATIONS_EMPTY_SPAN))
        notification = profile_page.find(profile_page.Locators.NOTIFICATIONS_EMPTY_SPAN)
      
        assert notification.text == 'Новых уведомлений нет.'

        profile_page.delete_post()
        second_driver.quit()
