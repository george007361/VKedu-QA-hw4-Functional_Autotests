import pytest
from selenium.webdriver import Keys, ActionChains
from leonard.utils.locators import BasePageLocators
from leonard.utils.base_case import BaseCase
from leonard.pages.profile_page import ProfilePage
from leonard.utils.help import RandomText


class TestCreationPost(BaseCase):

    @pytest.fixture(autouse=True, scope='function')
    def profile(self, setup, profileID):
        self.currentPage = ProfilePage(
            self.driver, profileID(self.asAuthor), True)

    @pytest.fixture(scope='function')
    def openCreator(self, profile):
        self.currentPage.ClickPostCreateBtn()
        post = self.currentPage.GetCreatedPost()
        return post

    def test_create_open(self):
        self.currentPage.ClickPostCreateBtn()
        post = self.currentPage.GetLastPost()
        content = self.currentPage.GetPostContent(post)
        assert content.get_attribute('contenteditable') == 'true'

    def test_create_close(self, openCreator):
        content = self.currentPage.GetPostContent(openCreator)

        self.currentPage.ClickPostCreateBtn()
        self.currentPage.CheckStaleness(content)

    def test_create_cancel(self, openCreator):
        savedText = RandomText(10)
        content = self.currentPage.GetPostContent(openCreator)

        content.clear()
        content.send_keys(savedText)
        self.currentPage.ClickPostCancelBtn(openCreator)

        self.currentPage.CheckStaleness(openCreator)
        lastPost = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(lastPost).text != savedText

    def test_create_save(self, openCreator):
        savedText = RandomText(100)
        content = self.currentPage.GetPostContent(openCreator)

        content.clear()
        content.send_keys(savedText)
        self.currentPage.ClickPostSubmitBtn(openCreator)

        lastPost = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(lastPost).text == savedText

    def test_create_empty(self, openCreator):
        content = self.currentPage.GetPostContent(openCreator)

        content.clear()
        self.currentPage.ClickPostSubmitBtn(openCreator, aTimeout=0)

        assert self.currentPage.GetCreatedPost().is_displayed() == True
        assert self.currentPage.Find(
            BasePageLocators().NOTICE_LAST
        ).text == "Длина поста должна быть в пределах от 1 до 10000"

    @ pytest.mark.xfail
    def test_hotkey_save(self, openCreator):
        savedText = RandomText(100)
        content = self.currentPage.GetPostContent(openCreator)

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
        content = self.currentPage.GetPostContent(openCreator)

        content.clear()
        self.currentPage.UploadImage(
            openCreator,
            'hw/code/leonard/uploads/test-image.jpg',
            20
        )
        savedText = content.text
        self.currentPage.ClickPostSubmitBtn(openCreator)

        lastPost = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(lastPost).text == savedText
