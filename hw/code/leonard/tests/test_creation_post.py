import time
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys, ActionChains
from leonard.utils.locators import BasePageLocators
from leonard.utils.base_case import BaseCase
from leonard.pages.profile_page import ProfilePage
from leonard.utils.help import RandomText

'''
Создание поста. Создание поста с картинкой в текст.
Создание поста. Создание поста с ограниченным доступом.
'''


class TestCreationPost(BaseCase):

    @pytest.fixture(autouse=True, scope='function')
    def profile(self, setup, profileID):
        self.driver.get('https://vdonate.ml/profile?id=' + profileID)
        self.currentPage = ProfilePage(self.driver, profileID)

    @pytest.fixture(scope='function')
    def openCreator(self, profile):
        self.currentPage.ClickPostCreateBtn()

    def test_create_open(self):
        self.currentPage.ClickPostCreateBtn()
        assert self.currentPage.GetLastPostContent()\
            .get_attribute('contenteditable') == 'true'

    def test_create_close(self, openCreator):
        self.currentPage.ClickPostCreateBtn()
        with pytest.raises(TimeoutException):
            self.currentPage.GetCreatePostContent()

    def test_create_cancel(self, openCreator):
        savedText = RandomText(10)
        self.currentPage.GetCreatePostContent().clear()
        self.currentPage.GetCreatePostContent().send_keys(savedText)
        self.currentPage.ClickPostCreaterCanselBtn()
        with pytest.raises(TimeoutException):
            self.currentPage.GetCreatePostContent()
        assert self.currentPage.GetLastPostContent().text != savedText

    def test_create_save(self, openCreator):
        savedText = RandomText(100)
        self.currentPage.GetCreatePostContent().clear()
        self.currentPage.GetCreatePostContent().send_keys(savedText)
        self.currentPage.ClickPostCreaterSubmitBtn()
        assert self.currentPage.GetLastPostContent()\
            .get_attribute('contenteditable') == None
        assert self.currentPage.GetLastPostContent().text == savedText

    def test_create_empty(self, openCreator):
        self.currentPage.GetCreatePostContent().clear()
        self.currentPage.ClickPostCreaterSubmitBtn(timeout=0)
        assert self.currentPage.GetLastPostContent()\
            .get_attribute('contenteditable') == 'true'
        assert self.currentPage.Find(
            BasePageLocators().NOTICE_LAST
        ).text == "Длина поста должна быть в пределах от 1 до 10000"

    @pytest.mark.xfail
    def test_hotkey_save(self, openCreator):
        savedText = RandomText(100)
        self.currentPage.GetCreatePostContent().clear()
        self.currentPage.GetCreatePostContent().send_keys(savedText)
        ActionChains(self.driver)\
            .key_down(Keys.CONTROL)\
            .send_keys(Keys.ENTER)\
            .perform()
        assert self.currentPage.GetLastPostContent()\
            .get_attribute('contenteditable') == 'false'
        assert self.currentPage.GetLastPostContent().text == savedText
