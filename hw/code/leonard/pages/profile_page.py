import os
from leonard.utils.locators import ProfilePageLocators
from leonard.utils.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select


class ProfilePage(BasePage):
    url = 'https://vdonate.ml/profile?id='
    locators = ProfilePageLocators()

    def __init__(self, driver, aID: int, aLoad=False):
        self.url += str(aID)
        super().__init__(driver, aLoad)

    def GetAboutContent(self):
        return self.Find(self.locators.ABOUT_CONTENT)

    def GetCreatedPost(self):
        return self.Find(self.locators.POST_CREATED)

    def GetLastPost(self):
        return self.Find(self.locators.POST_LAST)

    def GetPostContent(self, aPost):
        return self.FindIn(aPost, self.locators.POST_CONTENT)

    def GetSelectTierFromPost(self, aPost: WebElement):
        selectElement = self.FindIn(
            aPost, self.locators.POST_SELECTOR_TIER)
        return Select(selectElement)

    def GetPostNotAllowedElem(self, aPost: WebElement):
        return self.FindIn(aPost, self.locators.POST_NOT_ALLOWED)

    def ClickAboutEditBtn(self):
        self.Click(self.locators.ABOUT_EDIT_BTN)

    def ClickAboutCancelBtn(self):
        self.Click(self.locators.ABOUT_CANCEL_BTN)

    def ClickAboutSubmitBtn(self, aTimeout=5):
        self.ClickAndWait(
            self.locators.ABOUT_SUBMIT_BTN,
            aTimeout,
            EC.text_to_be_present_in_element_attribute(
                self.locators.ABOUT_CONTENT, 'contenteditable', 'false'
            )
        )

    def ClickPostCreateBtn(self):
        self.Click(self.locators.POST_CREATE_BTN)

    def ClickPostSubmitBtn(self, aPost, aTimeout=5):
        submit = self.FindIn(aPost, self.locators.POST_SUBMIT_BTN)
        self.ClickAndWait(
            submit,
            aTimeout,
            EC.all_of(
                EC.invisibility_of_element_located(self.locators.POST_CREATED),
                EC.any_of(
                    EC.text_to_be_present_in_element_attribute(
                        self.locators.POST_LAST_CONTENT,
                        'contenteditable',
                        'false'
                    ),
                    EC.none_of(
                        EC.element_attribute_to_include(
                            self.locators.POST_LAST_CONTENT,
                            'contenteditable'
                        )
                    )
                )
            )
        )

    def ClickPostCancelBtn(self, aPost):
        cancel = self.FindIn(aPost, self.locators.POST_CANCEL_BTN)
        self.Click(cancel)

    def ClickPostDeleteBtn(self, aPost):
        cancel = self.FindIn(aPost, self.locators.POST_DELETE_BTN)
        self.Click(cancel)

    def ClickPostEditBtn(self, aPost):
        cancel = self.FindIn(aPost, self.locators.POST_EDIT_BTN)
        self.Click(cancel)

    def UploadImage(self, aPost, aFilePath, aTimeout=5):
        imgCountBefore = len(
            self.FindIn(aPost, self.locators.POST_CONTENT)
                .find_elements(*self.locators.POST_IMAGES)
        )
        if (aFilePath[0] != '/'):
            aFilePath = os.path.abspath(aFilePath)
        self.FindIn(aPost, self.locators.POST_LOAD_FILE, visibility=False)\
            .send_keys(aFilePath)
        self.Wait(aTimeout).until(
            lambda _:
                len(
                    self.FindIn(aPost, self.locators.POST_CONTENT)
                    .find_elements(*self.locators.POST_IMAGES)
                ) == imgCountBefore + 1
        )
