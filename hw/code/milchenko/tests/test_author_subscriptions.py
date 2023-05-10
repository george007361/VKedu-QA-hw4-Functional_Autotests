import pytest
from selenium.webdriver.support import expected_conditions as EC

from milchenko.pages.author_subscriptions_page import AuthorSubscriptionsPage
from milchenko.tests.base_case import BaseCase

class TestAuthorSubscriptions(BaseCase):
    authorize = True

    # Создание авторской подписки. Нажатие плюса около "Уровни подписок" приводит к появлению модального окна с пустыми формами для заполнения
    def test_open_subscriptions(self):
        sub_page = AuthorSubscriptionsPage(self.browser)
        sub_page.open()
        sub_page.open_subs()
        assert sub_page.find(sub_page.Locators.SUBSCRIPTION_TITLE).text == 'Создание подписки'

    # # Создание авторской подписки. Модальное окно закрывается при нажатии крестика
    def test_close_by_cross(self):
        sub_page = AuthorSubscriptionsPage(self.browser)
        sub_page.open()
        sub_page.open_subs()
        sub_page.close_subs()
        assert sub_page.find(sub_page.Locators.SUBSCRIPTIONS_LEVEL).text == 'Уровни подписок'

    # # Создание авторской подписки. Модальное окно закрывается при нажатии кнопки Отменить в окне
    def test_close_by_cancel(self):
        sub_page = AuthorSubscriptionsPage(self.browser)
        sub_page.open()
        sub_page.open_subs()
        sub_page.close_subs(is_cross=False)
        assert sub_page.find(sub_page.Locators.SUBSCRIPTIONS_LEVEL).text == 'Уровни подписок'

    # Создание авторской подписки. Заголовок валидируется при количестве символов в нем не менее единицы и не более 30;
    # Создание авторской подписки. При наличии спецсимволов в заголовке появляется ошибка, согнализирующая об этом;
    # Создание авторской подписки. Стоимость валидируется при сумме, меньшей 1000000000 и большей 5 рублей;
    # Создание авторской подписки. Текст валидируется при количестве символов больше 1 и меньше 128;
    # Создание авторской подписки. При отсутствии картинки подписка успешно создается
    @pytest.mark.parametrize(
        'title, price, text, err',
        [
            (
                'Title',
                '200',
                'text',
                ''
            ),
            (
                '',
                '200',
                'text',
                'Символов в заголовке меньше 1'
            ),
            (
                'Title',
                '',
                'text',
                'Укажите цену не меньше 1'
            ),
            (
                'Title',
                '200',
                '',
                'Символов в тексте меньше 1'
            ),
            (
                'dfkoafiaposndvpnvsaoidfkoafiaposndvpnvsaoi',
                '200',
                'text',
                'Символов в заголовке больше 30'
            ),
            (
                'Title',
                '100000000000000000000',
                'text',
                'Укажите цену не больше 1000000000'
            ),
            (
                'Title',
                '200',
                'wqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjao',
                'Символов в тексте больше 128'
            ),
        ]
    )
    def test_create_subs(self, title, price, text, err):
        sub_page = AuthorSubscriptionsPage(self.browser)
        sub_page.open()
        sub_page.open_subs()
        sub_page.create_subscription(title, price, text)

        if err != "":
            assert sub_page.find(sub_page.Locators.FIRST_POPUP).text == err
        else:
            assert sub_page.is_clickable(sub_page.Locators.CREATE_BUTTON)
            sub_page.delete_subscription()
            sub_page.open_subs()

    # Изменение/удаление авторской подписки. Возможность поменять любое поле подписки
    # Изменение/удаление авторской подписки. Поведение при валидации идентично правилам при создании подписки (см. 14-17 пункты)
    @pytest.mark.parametrize(
        'title, price, text, err',
        [
            (
                'Title',
                '200',
                'text',
                ''
            ),
            (
                'dfkoafiaposndvpnvsaoidfkoafiaposndvpnvsaoi',
                '200',
                'text',
                'Символов в заголовке больше 30'
            ),
            (
                'Title',
                '100000000000000000000',
                'text',
                'Укажите цену не больше 1000000000'
            ),
            (
                'Title',
                '200',
                'wqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjaowqeasdkas;odjao',
                'Символов в тексте больше 128'
            ),
        ]
    )
    def test_update_subscription(self, title, price, text, err):
        sub_page = AuthorSubscriptionsPage(self.browser)
        sub_page.open()
        sub_page.open_subs()
        sub_page.create_subscription('qwerty', '123', 'asdfg')

        sub_page.open_update()
        sub_page.create_subscription(title, price, text, update=True)
        
        if err != "":
            assert sub_page.find(sub_page.Locators.FIRST_POPUP).text == err
            sub_page.close_subs()
        else:
            sub_page.open_subs()
            sub_page.close_subs()
            assert sub_page.find(sub_page.Locators.FIELD_TITLE).text == title
            assert sub_page.find(sub_page.Locators.FIELD_PRICE).text == price + '₽'
            assert sub_page.find(sub_page.Locators.FIELD_TEXT).text == text

        sub_page.delete_subscription()
        sub_page.open_subs()
        sub_page.close_subs()

    # Изменение/удаление авторской подписки. Возможность удалить подписку
    def test_delete_subscription(self):
        sub_page = AuthorSubscriptionsPage(self.browser)
        sub_page.open()
        sub_page.open_subs()
        sub_page.create_subscription("abc", "123", "abc")
        sub_page.delete_subscription()
        sub_page.open_subs()
        sub_page.close_subs()
        assert sub_page.find(sub_page.Locators.EMPTY_SUBSCRIPTIONS).text == 'У Вас нет платных подписок, но их можно создать по кнопке выше.'