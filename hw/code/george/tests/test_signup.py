import pytest

from base_case import BaseCase
from george.pages.signup_page import SignupPage
from george.helpers.random_data import RandomData
from george.helpers.popup_notifications import PopupNotification
from george.helpers.redirects import Redirect

# @pytest.mark.skip()
class TestSignup(BaseCase):
    authorize = False

    class CaseData:
        def __init__(self, email, nick, passwd, msg='', passwd_repeat=''):
            self.email = email
            self.nick = nick
            self.passwd = passwd
            self.msg = msg
            self.passwd_repeat = passwd if passwd_repeat == '' else passwd_repeat

    @pytest.mark.parametrize('case',
                             [
                                 # Ошибка при вводе нелатинских букв в email
                                 CaseData('русская@почта.ру', RandomData.string(10,
                                                                                RandomData.latin), '12345678', "Неверная почта"),

                                 # Ошибка при вводе более 255 символов после собаки в email
                                 CaseData(RandomData.string(20, RandomData.latin)+'@'+RandomData.string(260, RandomData.latin) + \
                                          '.ru', RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),

                                 # Ошибка при вводе более 64 символов до собаки в email
                                 CaseData(RandomData.string(70, RandomData.latin)+'@mail.ru',
                                          RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),

                                 # Ошибка при отсутствии собаки в email
                                 CaseData(RandomData.string(70, RandomData.latin) + '.ru',
                                          RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),

                                 # Ошибка при отсутствии точки в домене email
                                 CaseData(RandomData.string(70, RandomData.latin) + '@mailru',
                                          RandomData.string(10, RandomData.latin), '12345678', "Неверная почта"),

                                 # Ошибка при слишком длинном никнейме (более 20 символов)
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(21,
                                                                                                                RandomData.latin), '12345678', "Символов в псевдониме больше 20"),

                                 # Ошибка при слишком коротком никнейме (менее 3 символов)
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(2,
                                                                                                                RandomData.latin), '12345678', "Символов в псевдониме меньше 3"),

                                 # Ошибка при запрещенных символах в никнейме (все, кроме латиницы, кириллицы, чисел, нижнего подчеркивания и пробела)
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru',
                                          'я_test 007 #-+)(%$!@', '12345678', "В псевдониме разрешены"),

                                 # Ошибка при коротком пароле (менее 5 символов)
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10,
                                                                                                                RandomData.latin), RandomData.string(4, RandomData.latin), "Символов в пароле меньше"),

                                 # Ошибка при длинном пароле (более 30 символов)
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10,
                                                                                                                RandomData.latin), RandomData.string(31, RandomData.latin), "Символов в пароле больше"),

                                 # Ошибка при запрещенных символах в пароле (все, кроме латиницы, чисел, ! @ # $ % ^ & * _ и пробела)
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10,
                                                                                                                RandomData.latin), 'pass123!@#$%^&*_ ()+=', "В пароле разрешены"),

                                 # Ошибка при неверном вводе повтора пароля
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10,
                                                                                                                RandomData.latin), '12345678', "Поле повторного пароля должно совпадать", '87654321'),
                             ])
    def test_signup_fail(self, case: CaseData):
        register_page = SignupPage(self.browser)
        register_page.signup(case.email, case.nick,
                             case.passwd, case.passwd_repeat)
        Redirect.not_redirected(register_page)
        PopupNotification.exists(register_page, case.msg)

    @pytest.mark.parametrize('case',
                             [
                                 # Регистрация с обычными данными
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru',
                                          RandomData.string(10, RandomData.latin), '12345678'),
                                 
                                 # Почта с разрешенными символами ! # $ % & ' * + - / = ? ^ _ ` { | } ~
                                 CaseData(RandomData.string(5, RandomData.latin)+ '!#$%&\'*+-/=?^_`{|}~@mail.ru', RandomData.string(10, RandomData.latin), '12345678'),
                                 
                                 # Ник с разрешенными символами латиницы, кириллицы, чисел, нижнего подчеркивания и пробела
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(3, RandomData.latin) + 'а_б 1_2', '12345678'),
                                 
                                 # Пароль с разрешенными символами латиницы, чисел, ! @ # $ % ^ & * _ и пробела
                                 CaseData(RandomData.string(12, RandomData.latin)+'@mail.ru', RandomData.string(10, RandomData.latin), 'abc 123!@#$%^&*_'),
                             ])
    def test_signup_success(self, case: CaseData):
        register_page = SignupPage(self.browser)
        register_page.signup(case.email, case.nick,
                             case.passwd, case.passwd)
        Redirect.redirected(register_page)
