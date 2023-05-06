
import pytest
from pages.signup_page import SignupPage
from helpers.random_data import RandomData
from helpers.popup_notifications import PopupNotification
from helpers.redirects import Redirect


class Case:
    def __init__(self, email, nick, passwd, msg='', passwd_repeat=''):
        self.email = email
        self.nick = nick
        self.passwd = passwd
        self.msg = msg
        self.passwd_repeat = passwd if passwd_repeat == '' else passwd_repeat 


def test_signup_success(browser):
    cases = [
        Case(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10, RandomData.latin), '12345678'),
    ]
    for case in cases:
        register_page = SignupPage(browser)
        register_page.signup(case.email, case.nick, case.passwd, case.passwd)
        Redirect.redirected(register_page)

def test_signup_fail(browser):
    cases = [
        # Ошибка при вводе нелатинских букв в email
        Case('русская@почта.ру', RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),
        
        # Ошибка при вводе более 255 символов после собаки в email
        Case(RandomData.string(20, RandomData.latin)+'@'+RandomData.string(260, RandomData.latin)+'.ru', RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),
        
        # Ошибка при вводе более 64 символов до собаки в email
        Case(RandomData.string(70, RandomData.latin)+'@mail.ru', RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),
        
        # Ошибка при отсутствии собаки в email
        Case(RandomData.string(70, RandomData.latin) + '.ru', RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),
    
        # Ошибка при отсутствии точки в домене email
        Case(RandomData.string(70, RandomData.latin) + '@mailru', RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),

        # Ошибка при слишком длинном никнейме (более 20 символов)
        Case(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(21, RandomData.latin), '12345678', "Символов в псевдониме больше 20"),

        # Ошибка при слишком коротком никнейме (менее 3 символов)
        Case(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(2, RandomData.latin), '12345678', "Символов в псевдониме меньше 3"),

        # Ошибка при запрещенных символах в никнейме (все, кроме латиницы, кириллицы, чисел, нижнего подчеркивания и пробела)
        Case(RandomData.string(12, RandomData.latin)+'@mail.ru', 'я_test 007 #-+)(%$!@', '12345678', "В псевдониме разрешены"),

        # Ошибка при коротком пароле (менее 5 символов)
        Case(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10, RandomData.latin), RandomData.string(4, RandomData.latin), "Символов в пароле меньше"),

        # Ошибка при длинном пароле (более 30 символов)
        Case(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10, RandomData.latin), RandomData.string(31, RandomData.latin), "Символов в пароле больше"),

        # Ошибка при запрещенных символах в пароле (все, кроме латиницы, чисел, ! @ # $ % ^ & * _ и пробела)
        Case(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10, RandomData.latin), 'pass123!@#$%^&*_ ()+=', "В пароле разрешены"),

        # Ошибка при неверном вводе повтора пароля
        Case(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10, RandomData.latin), '12345678', "Поле повторного пароля должно совпадать", '87654321'),
    ]

    for case in cases:
        register_page = SignupPage(browser)       
        register_page.signup(case.email, case.nick, case.passwd, case.passwd_repeat)
        Redirect.not_redirected(register_page)
        PopupNotification.exists(register_page, case.msg)
