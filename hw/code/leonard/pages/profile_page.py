import time
from leonard.utils.locators import ProfilePageLocators
from leonard.utils.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class ProfilePage(BasePage):
    url = 'https://vdonate.ml/profile?id='
    locators = ProfilePageLocators()

    def __init__(self, driver, aID: int):
        self.url += str(aID)
        super().__init__(driver)

    def GetAboutContent(self):
        return self.Find(self.locators.ABOUT_CONTENT)

    def GetCreatePostContent(self):
        return self.Find(self.locators.POST_CREATE_CONTENT)

    def GetLastPostContent(self):
        return self.Find(self.locators.POST_LAST)

    def ClickAboutEditBtn(self):
        self.Click(self.locators.ABOUT_EDIT_BTN)

    def ClickAboutCancelBtn(self):
        self.Click(self.locators.ABOUT_CANCEL_BTN)

    def ClickAboutSubmitBtn(self, timeout=5):
        self.ClickAndWait(
            self.locators.ABOUT_SUBMIT_BTN,
            timeout,
            EC.text_to_be_present_in_element_attribute(
                self.locators.ABOUT_CONTENT, 'contenteditable', 'false'
            )
        )

    def ClickPostCreateBtn(self):
        self.Click(self.locators.POST_CREATE_BTN)

    def ClickPostCreaterSubmitBtn(self, timeout=5):
        self.ClickAndWait(
            self.locators.POST_CREATER_SUBMIT_BTN,
            timeout,
            EC.invisibility_of_element_located(
                self.locators.POST_CREATE_CONTENT
            )
        )

    def ClickPostCreaterCanselBtn(self):
        self.Click(self.locators.POST_CREATER_CANCEL_BTN)
