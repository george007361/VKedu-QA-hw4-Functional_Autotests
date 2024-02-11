import pytest
from selenium.webdriver import Keys, ActionChains
from leonard.utils.locators import BasePageLocators
from leonard.utils.base_case import BaseCase
from leonard.pages.profile_page import ProfilePage
from leonard.utils.help import RandomText


class TestEditPost(BaseCase):
    authorize = True

    @pytest.fixture(autouse=True, scope='function')
    def profile(self, setup, profileID):
        self.currentPage = ProfilePage(
            self.driver, profileID(self.asAuthor), True)

    @pytest.fixture(scope='function')
    def lastPostEditor(self, profile):
        post = self.currentPage.GetLastPost()
        self.currentPage.ClickPostEditBtn(post)
        return post

    @pytest.fixture(scope='function')
    def createPostWithImage(self, profile):
        self.currentPage.ClickPostCreateBtn()
        post = self.currentPage.GetCreatedPost()
        content = self.currentPage.GetPostContent(post)

        content.clear()
        self.currentPage.UploadImage(
            post,
            'hw/code/leonard/uploads/test-image.jpg',
            20
        )
        self.currentPage.ClickPostSubmitBtn(post)

    @pytest.fixture(scope='function')
    def createPostWithText(self, profile):
        self.currentPage.ClickPostCreateBtn()
        post = self.currentPage.GetCreatedPost()
        content = self.currentPage.GetPostContent(post)
        savedText = RandomText(100)

        content.clear()
        content.send_keys(savedText)
        self.currentPage.ClickPostSubmitBtn(post)

    def test_editor_open(self):
        post = self.currentPage.GetLastPost()
        self.currentPage.ClickPostEditBtn(post)
        assert self.currentPage.GetPostContent(post)\
            .get_attribute('contenteditable') == 'true'

    def test_editor_close(self, lastPostEditor):
        self.currentPage.ClickPostEditBtn(lastPostEditor)
        assert self.currentPage.GetAboutContent().get_attribute(
            'contenteditable') == 'false'

    def test_cancel(self):
        cancelText = RandomText(100)
        post = self.currentPage.GetLastPost()
        content = self.currentPage.GetPostContent(post)
        currentText = content.text

        self.currentPage.ClickPostEditBtn(post)
        content.send_keys(cancelText)
        self.currentPage.ClickPostCancelBtn(post)

        assert content.text == currentText

    def test_delete_image(self, createPostWithImage, lastPostEditor):
        savedText = RandomText(100)
        content = self.currentPage.GetPostContent(lastPostEditor)

        content.send_keys(Keys.END + Keys.BACKSPACE)
        content.send_keys(savedText)
        self.currentPage.ClickPostSubmitBtn(lastPostEditor)

        post = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(post).text == savedText

    def test_delete_all_in_post(self, createPostWithText, lastPostEditor):
        content = self.currentPage.GetPostContent(lastPostEditor)

        ActionChains(self.driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('a')\
            .perform()
        content.send_keys(Keys.BACKSPACE)
        self.currentPage.ClickPostSubmitBtn(lastPostEditor, aTimeout=0)

        assert self.currentPage.GetLastPost().is_displayed() == True
        assert self.currentPage.Find(
            BasePageLocators().NOTICE_LAST
        ).text == "Длина поста должна быть в пределах от 1 до 10000"

    def test_post(self, createPostWithText, lastPostEditor):
        content = self.currentPage.GetPostContent(lastPostEditor)
        postText = content.text

        self.currentPage.ClickPostDeleteBtn(lastPostEditor)

        self.currentPage.CheckStaleness(lastPostEditor)

        lastPost = self.currentPage.GetLastPost()
        assert self.currentPage.GetPostContent(lastPost).text != postText
