import pytest
from selenium.common.exceptions import TimeoutException
from leonard.utils.locators import ProfilePageLocators
from leonard.utils.base_case import BaseDualCase
from leonard.pages.profile_page import ProfilePage
from leonard.utils.help import RandomText
from selenium.webdriver.common.by import By

subscriptionNames = ['Новости', 'Мемы', 'Вакансии']


class TestPostLimitation(BaseDualCase):

    def CountAuthorPosts(self):
        posts = self.donatorPage.Find(
            self.donatorPage.locators.POSTS_CONTAINER)
        return len(posts.find_elements(*ProfilePageLocators.POST_CONTENT))

    def GenLimitLable(self, id):
        return 'Доступно по подписке ' + subscriptionNames[id - 1]

    def CreatePostWithText(self, aTierId: int):
        self.authorPage.ClickPostCreateBtn()
        post = self.authorPage.GetCreatedPost()
        content = self.authorPage.GetPostContent(post)
        savedText = RandomText(100)

        content.clear()
        content.send_keys(savedText)
        select = self.authorPage.GetSelectTierFromPost(post)
        select.select_by_index(aTierId)

        self.authorPage.ClickPostSubmitBtn(post)

    @pytest.fixture(autouse=True, scope='function')
    def profile(self, setup, profileID):
        self.authorPage = ProfilePage(self.authorDriver, profileID(True), True)
        self.donatorPage = ProfilePage(
            self.donatorDriver, profileID(True), True)

    @pytest.fixture(scope='function')
    def openCreator(self, profile):
        self.authorPage.ClickPostCreateBtn()
        post = self.authorPage.GetCreatedPost()
        return post

    @pytest.mark.parametrize('aID', [2, 3])
    def test_creat_post_with_limitation(self, openCreator, aID):
        beforePostsCount = self.CountAuthorPosts()
        savedText = RandomText(100)
        content = self.authorPage.GetPostContent(openCreator)
        content.clear()
        content.send_keys(savedText)
        select = self.authorPage.GetSelectTierFromPost(openCreator)
        select.select_by_index(aID)
        self.authorPage.ClickPostSubmitBtn(openCreator)
        # Проверка на стороне автора
        post = self.authorPage.GetLastPost()
        self.authorPage.ClickPostEditBtn(post)
        select2 = self.authorPage.GetSelectTierFromPost(post)
        [option] = select2.all_selected_options
        assert option.get_attribute("value") == str(aID)
        # Проверка на стороне подписчика
        self.donatorPage.Reload()

        afterPostsCount = self.CountAuthorPosts()
        assert afterPostsCount == beforePostsCount + 1

        lastPost = self.donatorPage.GetLastPost()
        assert self.donatorPage.GetPostNotAllowedElem(lastPost).find_element(
            By.TAG_NAME, 'span').text == self.GenLimitLable(aID)

    @pytest.mark.parametrize('aOldId, aNewId', [
        pytest.param(0, 2, marks=pytest.mark.xfail),
        pytest.param(1, 3, marks=pytest.mark.xfail),
    ])
    def test_raise_post_limitation(self, aOldId, aNewId):
        self.CreatePostWithText(aOldId)
        post = self.authorPage.GetLastPost()
        self.authorPage.ClickPostEditBtn(post)

        select = self.authorPage.GetSelectTierFromPost(post)
        select.select_by_index(aNewId)
        self.authorPage.ClickPostSubmitBtn(post)
        # Проверка на стороне автора
        post = self.authorPage.GetLastPost()
        self.authorPage.ClickPostEditBtn(post)
        select2 = self.authorPage.GetSelectTierFromPost(post)
        [option] = select2.all_selected_options
        assert option.get_attribute("value") == str(aNewId)
        # Проверка на стороне подписчика
        self.donatorPage.Reload()
        self.donatorPage.GetLastPost()

        lastPost = self.donatorPage.GetLastPost()
        assert self.donatorPage.GetPostNotAllowedElem(lastPost).find_element(
            By.TAG_NAME, 'span').text == self.GenLimitLable(aNewId)

    @pytest.mark.parametrize('aOldId, aNewId', [
        pytest.param(3, 1, marks=pytest.mark.xfail),
        pytest.param(2, 0, marks=pytest.mark.xfail)
    ])
    def test_decrease_post_limitation(self, aOldId, aNewId):
        self.CreatePostWithText(aOldId)
        post = self.authorPage.GetLastPost()
        self.authorPage.ClickPostEditBtn(post)

        select = self.authorPage.GetSelectTierFromPost(post)
        select.select_by_index(aNewId)
        self.authorPage.ClickPostSubmitBtn(post)
        # Проверка на стороне автора
        post = self.authorPage.GetLastPost()
        self.authorPage.ClickPostEditBtn(post)
        select2 = self.authorPage.GetSelectTierFromPost(post)
        [option] = select2.all_selected_options
        assert option.get_attribute("value") == str(aNewId)
        # Проверка на стороне подписчика
        self.donatorPage.Reload()
        self.donatorPage.GetLastPost()

        lastPost = self.donatorPage.GetLastPost()
        with pytest.raises(TimeoutException):
            self.donatorPage.GetPostNotAllowedElem(lastPost)
