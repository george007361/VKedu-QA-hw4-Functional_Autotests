import pytest
import os

from base_case import BaseCase
from pages.signin_page import SigninPage
from helpers.popup_notifications import PopupNotification
from helpers.redirects import Redirect

@pytest.mark.skip()
class TestSignin(BaseCase):
    authorize = False

    class CaseData:
        def __init__(self, email, passwd, msg=''):
            self.email = email
            self.passwd = passwd
            self.msg = msg

    def test_signin_success(self):
        login_page = SigninPage(self.browser)
        login_page.signin(os.environ["LOGIN"], os.environ["PASSWORD"])
        Redirect.redirected(login_page)

    @pytest.mark.parametrize('case',
                             [
                                 # Несуществующий пользователь
                                 CaseData("not_exists", "12345678",
                                          'Неверный псевдоним'),

                                 # Неверный пароль
                                 CaseData(
                                     os.environ["LOGIN"], "wrong_password", 'Неверный пароль'),
                             ])
    def test_signin_fail(self, case : CaseData):
        login_page = SigninPage(self.browser)
        login_page.signin(case.email, case.passwd)
        Redirect.not_redirected(login_page)
        PopupNotification.exists(login_page, case.msg)