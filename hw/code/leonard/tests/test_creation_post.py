import time
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys, ActionChains
from leonard.utils.locators import BasePageLocators
from leonard.utils.base_case import BaseCase
from leonard.pages.profile_page import ProfilePage
from leonard.utils.help import RandomText

'''
Создание поста. Создание поста с ограниченным доступом.
'''


class TestCreationPost(BaseCase):

    @pytest.fixture(autouse=True, scope='function')
    def profile(self, setup, profileID):
        self.currentPage = ProfilePage(self.driver, profileID, True)

    @pytest.fixture(scope='function')
    def openCreator(self, profile):
        self.currentPage.ClickPostCreateBtn()

    def test_create_open(self):
        self.currentPage.ClickPostCreateBtn()
        post = self.currentPage.GetLastPost()
        content = self.currentPage.GetPostContent(post)
        assert content.get_attribute('contenteditable') == 'true'

    def test_create_close(self, openCreator):
        post = self.currentPage.GetCreatedPost()
        content = self.currentPage.GetPostContent(post)

        self.currentPage.ClickPostCreateBtn()
        self.currentPage.CheckStaleness(content)

    def test_create_cancel(self, openCreator):
        savedText = RandomText(10)
        post = self.currentPage.GetCreatedPost()
        content = self.currentPage.GetPostContent(post)

        content.clear()
        content.send_keys(savedText)
        self.currentPage.ClickPostCancelBtn(post)

        self.currentPage.CheckStaleness(post)
        lastPost = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(lastPost).text != savedText

    def test_create_save(self, openCreator):
        savedText = RandomText(100)
        post = self.currentPage.GetCreatedPost()
        content = self.currentPage.GetPostContent(post)

        content.clear()
        content.send_keys(savedText)
        self.currentPage.ClickPostSubmitBtn(post)

        lastPost = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(lastPost).text == savedText

    def test_create_empty(self, openCreator):
        post = self.currentPage.GetCreatedPost()
        content = self.currentPage.GetPostContent(post)

        content.clear()
        self.currentPage.ClickPostSubmitBtn(post, aTimeout=0)

        assert self.currentPage.GetCreatedPost().is_displayed() == True
        assert self.currentPage.Find(
            BasePageLocators().NOTICE_LAST
        ).text == "Длина поста должна быть в пределах от 1 до 10000"

    @ pytest.mark.xfail
    def test_hotkey_save(self, openCreator):
        savedText = RandomText(100)
        post = self.currentPage.GetCreatedPost()
        content = self.currentPage.GetPostContent(post)

        content.clear()
        content.send_keys(savedText)
        ActionChains(self.driver)\
            .key_down(Keys.CONTROL)\
            .send_keys(Keys.ENTER)\
            .perform()

        lastPost = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(lastPost)\
            .get_attribute('contenteditable') == 'false'
        assert self.currentPage.GetPostContent(lastPost).text == savedText

    def test_creation_with_image(self, openCreator):
        post = self.currentPage.GetCreatedPost()
        content = self.currentPage.GetPostContent(post)

        content.clear()
        self.currentPage.UploadImage(
            post,
            'hw/code/leonard/tests/test-image.jpg',
            20
        )
        savedText = content.text
        self.currentPage.ClickPostSubmitBtn(post)

        lastPost = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(lastPost).text == savedText

    # @ pytest.mark.parametrize('aOptionIdx', [])
    # def test_creation_with_limitation(self, openCreator, aOptionIdx):
    #     savedText = RandomText(100)
    #     post = self.currentPage.GetCreatedPost()
    #     content = self.currentPage.GetPostContent(post)

    #     content.clear()
    #     content.send_keys(savedText)
    #     select = self.currentPage.GetSelectTierFromPost(
    #         self.Find(self.currentPage.locators.POST_CREATED)
    #     )
    #     select.options
