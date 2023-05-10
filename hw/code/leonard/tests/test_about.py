import pytest
from selenium.webdriver import Keys, ActionChains
from leonard.utils.locators import BasePageLocators
from leonard.utils.base_case import BaseCase
from leonard.pages.profile_page import ProfilePage
from leonard.utils.help import RandomText

savePayload = [
    pytest.param(
        '',
        'Здесь будет информация о Вас.\nСкорее заполните ее, чтобы пользователи могли узнать о Вас больше.',
        marks=pytest.mark.xfail
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
    def profile(self, setup, profileID):
        self.currentPage = ProfilePage(
            self.driver, profileID(self.asAuthor), True)

    @pytest.fixture(scope='function')
    def openeEditor(self, profile):
        self.currentPage.ClickAboutEditBtn()

    def test_editor_open(self):
        self.currentPage.ClickAboutEditBtn()
        assert self.currentPage.GetAboutContent().get_attribute('contenteditable') == 'true'

    def test_editor_close(self, openeEditor):
        self.currentPage.ClickAboutEditBtn()
        assert self.currentPage.GetAboutContent().get_attribute(
            'contenteditable') == 'false'

    def test_cancel(self):
        cancelText = RandomText(10)
        currentText = self.currentPage.GetAboutContent().text
        self.currentPage.ClickAboutEditBtn()
        self.currentPage.GetAboutContent().send_keys(cancelText)
        self.currentPage.ClickAboutCancelBtn()
        assert self.currentPage.GetAboutContent().text == currentText

    @pytest.mark.parametrize('aInputText, aSavedText', savePayload)
    def test_save(self, openeEditor, aInputText, aSavedText):
        self.currentPage.GetAboutContent().clear()
        self.currentPage.GetAboutContent().send_keys(aInputText)
        self.currentPage.ClickAboutSubmitBtn()
        assert self.currentPage.GetAboutContent().text == aSavedText

    @pytest.mark.xfail
    def test_hotkey_save(self, openeEditor):
        savedText = RandomText(10)
        self.currentPage.GetAboutContent().clear()
        self.currentPage.GetAboutContent().send_keys(savedText)
        ActionChains(self.driver)\
            .key_down(Keys.CONTROL)\
            .send_keys(Keys.ENTER)\
            .perform()
        assert self.currentPage.GetAboutContent().get_attribute(
            'contenteditable') == 'false'
        assert self.currentPage.GetAboutContent().text == savedText

    def test_overload_save(self, openeEditor):
        savedText = RandomText(1001)
        self.currentPage.GetAboutContent().clear()
        self.currentPage.GetAboutContent().send_keys(savedText)
        self.currentPage.ClickAboutSubmitBtn(aTimeout=0)
        assert self.currentPage.GetAboutContent().get_attribute('contenteditable') == 'true'
        assert self.currentPage.Find(
            BasePageLocators().NOTICE_LAST
        ).text == "Поле 'Обо мне' должно содержать меньше 1000 символов"
