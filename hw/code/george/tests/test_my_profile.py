import pytest

from base_case import BaseCase

from george.helpers.random_data import RandomData
from george.pages.signup_page import SignupPage
from george.pages.feed_page import FeedPage
from george.pages.my_profile_page import MyProfilePage
from george.pages.user_profile_page import UserProfilePage

class TestUserProfile(BaseCase):
    authorize = False

    @pytest.fixture(scope='function', autouse=True)
    def create_user_profile(self, setup):
        self.email = RandomData.string(10, RandomData.latin) + '@mail.ru'
        self.nick = RandomData.string(10, RandomData.latin)
        self.passwd = RandomData.string(10, RandomData.latin)

        reg_page = SignupPage(self.browser)
        reg_page.signup(self.email, self.nick, self.passwd, self.passwd)

        feed_page = FeedPage(self.browser)
        self.my_url = feed_page.get_my_profile_link()

    # @pytest.mark.skip()
    def test_acount_is_user_by_default(self):
        my_page = MyProfilePage(self.browser, self.my_url)
        assert my_page.check_is_author() is False
    
    # @pytest.mark.skip()
    def test_change_account_to_be_author(self):
        my_page = MyProfilePage(self.browser, self.my_url)

        assert my_page.check_is_author() is False

        my_page.became_author()

        assert my_page.check_is_author() is True

    def test_subscription_to_user(self):
        test_user_page = UserProfilePage(self.browser, self.test_acc_link)

        assert test_user_page.is_followed() is False

        test_user_page.change_subscription()

        assert test_user_page.is_followed() is True

        test_user_page.change_subscription()

        assert test_user_page.is_followed() is False

        

    



        

        