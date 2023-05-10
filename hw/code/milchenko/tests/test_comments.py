from selenium.webdriver.support import expected_conditions as EC

from milchenko.tests.base_case import BaseCase
from milchenko.pages.profile_page import ProfilePage

class TestComments(BaseCase):
    authorize = True
    
    # Комментарии к постам. Нажатие кнопки комментариев приводит к появлению комментариев под постом
    def test_open_comments(self):
       profile_page = ProfilePage(self.browser)
       profile_page.open()
       profile_page.create_post(profile_page)

       profile_page.open_comments()

       assert profile_page.find(profile_page.Locators.COMMENT_FIELD)
       profile_page.delete_post()

    # Комментарии к постам. При повторном нажатии на кнопку комментариев они скрываются
    def test_close_comments(self):
       profile_page = ProfilePage(self.browser)
       profile_page.open()
       profile_page.create_post(profile_page)

       profile_page.open_comments()
       profile_page.close_comments()

       assert profile_page.is_clickable(profile_page.Locators.COMMENT_BUTTON)
       profile_page.delete_post()

    # Комментарии к постам. Комментарий успешно оставляется под постом при нажатии на кнопку Отправить
    def test_send_comment(self):
       profile_page = ProfilePage(self.browser)
       profile_page.open()
       profile_page.create_post(profile_page)

       profile_page.open_comments()
       profile_page.create_comment()

       assert profile_page.find(profile_page.Locators.COMMENT_TEXT).text == 'test'
       profile_page.delete_post()

    # Комментарии к постам. Возможность отправить комментарий с помощью сочетания клавиш Ctrl + Enter
    def test_hotkey_comment_sent(self):
       profile_page = ProfilePage(self.browser)
       profile_page.open()
       profile_page.create_post(profile_page)

       profile_page.open_comments()
       profile_page.create_comment(hotkey=True)

       assert profile_page.find(profile_page.Locators.COMMENT_TEXT).text == 'test'
       profile_page.delete_post()

    # Комментарии к постам. Ошибка при попытке отправить пустой комментарий
    def test_error_empty_comment(self):
       profile_page = ProfilePage(self.browser)
       profile_page.open()
       profile_page.create_post(profile_page)

       profile_page.open_comments()
       profile_page.send_empty_comment()

       assert profile_page.find(profile_page.Locators.ERR_EMPTY_COMMENT).text == 'Вы ввели пустой комментарий'
       profile_page.delete_post()

    # Комментарии к постам. Комментарий удаляется при нажатии автором на крестик рядом с ним
    def test_delete_comment_by_cross(self):
       profile_page = ProfilePage(self.browser)
       profile_page.open()
       profile_page.create_post(profile_page)

       profile_page.open_comments()
       profile_page.create_comment()

       profile_page.delete_comment()

       assert profile_page.find(profile_page.Locators.COMMENT_BUTTON).text == '0'
       profile_page.delete_post()