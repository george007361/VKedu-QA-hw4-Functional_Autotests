import time
import pytest
from selenium.webdriver import Keys, ActionChains
from leonard.utils.locators import BasePageLocators
from leonard.utils.base_case import BaseCase
from leonard.pages.profile_page import ProfilePage
from leonard.utils.help import RandomText

savePayload = [
    (
        '',
        'Здесь будет информация о Вас.\nСкорее заполните ее, чтобы пользователи могли узнать о Вас больше.'
    ),
    ('   Текст с внешними пробелами.   ', 'Текст с внешними пробелами.'),
    (
        'Текст до переноса строки.' + Keys.ENTER + 'Текст после переноса строки',
        'Текст до переноса строки.\nТекст после переноса строки'
    )
]


class TestAbout(BaseCase):
    authorize = True

    @pytest.fixture(autouse=True, scope='function')
    def profile(self, setup):
        self.driver.get('https://vdonate.ml/profile?id=9')
        self.currentPage = ProfilePage(self.driver, 9)

    @pytest.fixture(scope='function')
    def editabout(self, profile):
        self.currentPage.ClickAboutEditBtn()

    def test_editor_open(self):
        self.currentPage.ClickAboutEditBtn()
        assert self.currentPage.GetAbout().get_attribute('contenteditable') == 'true'

    def test_editor_close(self, editabout):
        self.currentPage.ClickAboutEditBtn()
        assert self.currentPage.GetAbout().get_attribute('contenteditable') == 'false'

    def test_cancel(self, editabout):
        cancelText = RandomText(10)
        currentText = self.currentPage.GetAbout().text
        self.currentPage.GetAbout().send_keys(cancelText)
        self.currentPage.ClickAboutCancelBtn()
        assert self.currentPage.GetAbout().text == currentText

    @pytest.mark.parametrize('aInputText, aSavedText', savePayload)
    def test_save(self, editabout, aInputText, aSavedText):
        self.currentPage.GetAbout().clear()
        self.currentPage.GetAbout().send_keys(aInputText)
        self.currentPage.ClickAboutSubmitBtn()
        assert self.currentPage.GetAbout().get_attribute('contenteditable') == 'false'
        assert self.currentPage.GetAbout().text == aSavedText

    def test_hotkey_save(self, editabout):
        savedText = RandomText(10)
        self.currentPage.GetAbout().clear()
        self.currentPage.GetAbout().send_keys(savedText)
        ActionChains(self.driver)\
            .key_down(Keys.CONTROL)\
            .send_keys(Keys.ENTER)\
            .perform()
        assert self.currentPage.GetAbout().get_attribute('contenteditable') == 'false'
        assert self.currentPage.GetAbout().text == savedText

    def test_overload_save(self, editabout):
        savedText = RandomText(1001)
        self.currentPage.GetAbout().clear()
        self.currentPage.GetAbout().send_keys(savedText)
        self.currentPage.ClickAboutSubmitBtn(timeout=0)
        assert self.currentPage.GetAbout().get_attribute('contenteditable') == 'true'
        assert self.currentPage.Find(
            BasePageLocators().NOTICE
        ).text == "Поле 'Обо мне' должно содержать меньше 1000 символов"
