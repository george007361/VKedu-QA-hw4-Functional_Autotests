import os

import pytest

from zenehu.pages.profile_page import ProfilePage
from zenehu.tests.base_case import BaseCase
from zenehu.utils.random_string import random_string


class TestProfile(BaseCase):
    authorize = True

    # Редактирование профиля. Ошибка при загрузке большого аватара
    @pytest.mark.parametrize(
        'avatar, expected_error', [
            (
                    'hw/code/zenehu/pages/assets/test_image.jpg', 'Ошибка сервера'
            ),
        ]
    )
    def test_edit_profile_avatar_error(self, avatar, expected_error):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        profile_page.edit_avatar(avatar)

        assert profile_page.find(profile_page.Locators.FIRST_POPUP).text == expected_error

        profile_page.close_popups()

    # Редактирование профиля. При успешном редактировании данные в профиле меняются
    def test_edit_profile_success_data(self):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        email = random_string(10) + "@" + random_string(5) + ".ru"
        profile_page.edit_profile(email, os.getenv("ALB_USERNAME"), os.getenv("ALB_PASSWORD"), os.getenv("ALB_PASSWORD"))

        profile_page.open_edit_page()

        assert profile_page.find(profile_page.Locators.PROFILE_EMAIL).get_attribute("value") == email

    # Редактирование профиля. Форма открывается нажатием на карандаш в профиле пользователя
    def test_edit_profile_open(self):
        page = ProfilePage(self.browser)
        page.open_edit_page()

        assert page.find(page.Locators.PROFILE_EDIT_CROSS_BUTTON)

    # Редактирование профиля. Форма закрывается кнопкой "Отменить"
    def test_edit_profile_close_cancel(self):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        profile_page.close_edit_page_cancel()

        assert profile_page.is_clickable(profile_page.Locators.PROFILE_EDIT_BUTTON)

    # Редактирование профиля. Форма закрывается при нажатии на крестик
    def test_edit_profile_close_cross(self):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        profile_page.close_edit_page_cross()

        assert profile_page.is_clickable(profile_page.Locators.PROFILE_EDIT_BUTTON)

    # Редактирование профиля. Ошибка при вводе нелатинских букв в email
    # Редактирование профиля. Ошибка при вводе длинной почты (более 320 символов в сумме)
    # Редактирование профиля. Ошибка при вводе более 255 символов в email после собаки
    # Редактирование профиля. Ошибка при вводе более 64 символов в email до собаки
    # Редактирование профиля. Ошибка при отсутствии собаки в email
    # Редактирование профиля. Ошибка при отсутствии точки в домене email
    # Редактирование профиля. Возможно установить очень короткий email (a@b.c)
    @pytest.mark.parametrize(
        'email, expected_error',
        [
            (
                    'абв@mail.ru',
                    "Неверная почта. До @ разрешены латиница, числа, символы !#$%&'*+-/=?^_`{|}~ и точка-разделитель"
            ),
            (
                    'wblsanfkgaejjpzjjemngnnosbyhetnemgcormdeevwewlgjeecfdxszjvqihixkbfzgkqptrpfbowrzrnwisslmbkhdcbpvxdkbhtrknwvftoiviznivuiurifeouzxetvlpunqzjrcnwaanyouoyzplaozusnodwpewecwmrmadvbxkevfyqtqbdjjfrejvpbfuuiygacxklkfanhfzxbzppvbayoezqkmsgojpaianiewntzgtsfjfyputpxu@ntgnaaedjkgbsszsbanedpqsgehljrkdmuiwvwluibvevqcugflliudmlfxxik.xk',
                    'Неверная почта. Символов до @ больше 64'
            ),
            (
                    'wblsanfkgaejjpzjjemngnnosbyhetnemgcormdeevwewlgjeecfdxszjvqihixkbfzgkqptrpfbowrzrnwisslmbkhdcbpvxdkbhtrknwvftoiviznivuiurifeouzxetvlpunqzjrcnwaanyouoyzplaozusnodwpewecwmrmadvbxkevfyqtqbdjjfrejvpbfuuiygacxklkfanhfzxbzppvbayoezqkmsgojpaianiewntzgtsfjfyputpxu@mail.ru',
                    'Неверная почта. Символов до @ больше 64'
            ),
            (
                    'abc@ntgnaaedjkgbsszsbanedpqsgehljrkdmuiwvwluibvevqcugfyllsiudmlfxxik.xk',
                    'Неверная почта. Символов после @ в одном подуровне больше 63'
            ),
            (
                    'abcmail.ru', 'Неверная почта. Пример: name@email.ru'
            ),
            (
                    'abc@mailru', 'Неверная почта. После @ должно быть минимум 2 подуровня'
            ),
            (
                    'a@b.c', ''
            )

        ]
    )
    def test_edit_profile_email_error(self, email, expected_error):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        profile_page.edit_profile(email, "", os.getenv("ALB_PASSWORD"), os.getenv("ALB_PASSWORD"))

        if expected_error:
            assert profile_page.find(profile_page.Locators.FIRST_POPUP).text == expected_error
            profile_page.close_popups()
        else:
            assert profile_page.is_clickable(profile_page.Locators.PROFILE_EDIT_BUTTON)

    # Редактирование профиля. Ошибка при вводе символов в email, отличных от ! # $ % & ' * + - / = ? ^ _ { | } ~ `
    @pytest.mark.parametrize(
        'email',
        [
            (
                    'a"@b.c'
            ),
            (
                    'a(@b.c'
            ),
            (
                    'a)@b.c'
            ),
            (
                    'a:@b.c'
            ),
            (
                    'a;@b.c'
            ),
            (
                    'a,@b.c'
            ),
            (
                    'a<@b.c'
            ),
            (
                    'a>@b.c'
            ),
        ]
    )
    def test_edit_profile_email_error_symbols(self, email):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        profile_page.edit_profile(email, "", os.getenv("ALB_PASSWORD"), os.getenv("ALB_PASSWORD"))

        assert profile_page.find(profile_page.Locators.FIRST_POPUP).text == \
               "Неверная почта. До @ разрешены латиница, числа, символы !#$%&'*+-/=?^_`{|}~ и точка-разделитель"

        profile_page.close_popups()

    # Редактирование профиля. Ошибка при слишком длинном никнейме (более 20 символов)
    # Редактирование профиля. Ошибка при слишком коротком никнейме (менее 3 символов)
    # Редактирование профиля. Ошибка при наличии запрещенных символов в никнейме (все, кроме латиницы, кириллицы, чисел, нижнего подчеркивания и пробела)
    @pytest.mark.parametrize(
        'username, expected_error',
        [
            (
                    'a' * 21, 'Символов в псевдониме больше 20'
            ),
            (
                    'a' * 2, 'Символов в псевдониме меньше 3'
            ),
            (
                    'a@b',
                    'В псевдониме разрешены латиница, кириллица, числа, знак нижнего подчеркивания и пробел между словами'
            ),
            (
                    'a!b',
                    'В псевдониме разрешены латиница, кириллица, числа, знак нижнего подчеркивания и пробел между словами'
            ),
            (
                    'a#b',
                    'В псевдониме разрешены латиница, кириллица, числа, знак нижнего подчеркивания и пробел между словами'
            ),
        ]
    )
    def test_edit_profile_username_error(self, username, expected_error):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        profile_page.edit_profile("", username, os.getenv("ALB_PASSWORD"), os.getenv("ALB_PASSWORD"))

        assert profile_page.find(profile_page.Locators.FIRST_POPUP).text == expected_error

        profile_page.close_popups()

    # Редактирование профиля. Ошибка при некорректном вводе пароля (символов либо меньше 5, либо больше 30)
    # Редактирование профиля. Ошибка при некорректном вводе пароля в поле "Повторите пароль" (либо не такой,
    # как в поле "Пароль", либо пустой)
    @pytest.mark.parametrize(
        'password, password_repeat, expected_error',
        [
            (
                    'a' * 4, 'a' * 4, 'Символов в пароле меньше 5'
            ),
            (
                    'a' * 31, 'a' * 31, 'Символов в пароле больше 30'
            ),
            (
                    'a' * 5, 'a' * 6, 'Поле повторного пароля должно совпадать с полем пароля'
            ),
            (
                    'a' * 5, '', 'Поле повторного пароля не может быть пустым'
            ),
        ]
    )
    def test_edit_profile_password_error(self, password, password_repeat, expected_error):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        profile_page.edit_profile("", "", password, password_repeat)

        assert profile_page.find(profile_page.Locators.FIRST_POPUP).text == expected_error

        profile_page.close_popups()

    # Редактирование профиля. При успешном редактировании форма закрывается
    def test_edit_profile_success(self):
        profile_page = ProfilePage(self.browser)
        profile_page.open_edit_page()

        email = random_string(10) + "@" + random_string(5) + ".ru"
        profile_page.edit_profile(email, os.getenv("ALB_USERNAME"),
                                  os.getenv("ALB_PASSWORD"),
                                  os.getenv("ALB_PASSWORD"))

        profile_page.is_clickable(profile_page.Locators.PROFILE_EDIT_BUTTON)
