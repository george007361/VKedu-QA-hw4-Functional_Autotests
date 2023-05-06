import pytest
from VDonate.pages.signin_page import SigninPage
import os
from VDonate.helpers.popup_notifications import PopupNotification
from VDonate.helpers.redirects import Redirect

class Case:
    def __init__(self, email, passwd, msg = ''):
        self.email = email
        self.passwd = passwd
        self.msg = msg


def test_signin_success(browser):
    login_page = SigninPage(browser)
    login_page.signin(os.environ["LOGIN"], os.environ["PASSWORD"])
    Redirect.redirected(login_page)

def test_signin_fail(browser):
    cases = [
        Case("not_exists", "12345678", 'Неверный псевдоним'),
        Case(os.environ["LOGIN"], "wrong_password", 'Неверный пароль')
    ]

    for case in cases:
        login_page = SigninPage(browser)
        login_page.signin(case.email, case.passwd)
        Redirect.not_redirected(login_page)
        PopupNotification.exists(login_page, case.msg)