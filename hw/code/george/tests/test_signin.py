import pytest
import os
from selenium.webdriver.support import expected_conditions as EC

from base_case import BaseCase

from george.pages.signin_page import SigninPage
from george.helpers.popup_notifications import PopupNotification
from george.helpers.redirects import Redirect

# @pytest.mark.skip()
class TestSignin(BaseCase):
    authorize = False

    class CaseData:
        def __init__(self, email, passwd, msg=''):
            self.email = email
            self.passwd = passwd
            self.msg = msg

    # @pytest.mark.skip()
    def test_signin_success(self):
        login_page = SigninPage(self.browser)
        login_page.signin(os.environ["GEORGE_LOGIN"], os.environ["GEORGE_PASSWORD"])
        Redirect.redirected(login_page)

    # @pytest.mark.skip()
    @pytest.mark.parametrize('case',
                             [
                                 # Несуществующий пользователь
                                 CaseData("not_exists", "12345678",
                                          'Неверный псевдоним'),

                                 # Неверный пароль
                                 CaseData(
                                     os.environ["GEORGE_LOGIN"], "wrong_password", 'Неверный пароль'),
                             ])
    def test_signin_fail(self, case : CaseData):
        login_page = SigninPage(self.browser)
        login_page.signin(case.email, case.passwd)
        login_page.wait().until(EC.element_to_be_clickable(login_page.Locators.LOGIN_BUTTON)        )
        Redirect.not_redirected(login_page)
        PopupNotification.exists(login_page, case.msg)
