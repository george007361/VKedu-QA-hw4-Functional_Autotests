from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

from milchenko.pages.base_page import BasePage

class ProfilePage(BasePage):
    base_url = 'https://vdonate.ml/feed'
    url: str

    class Locators:
        POST_DATA = (
            By.XPATH, '//div[@class="post__content post-content post-content__text font_regular"]'
        )
        PROFILE_BUTTON = (
            By.XPATH, '//img[contains(@class, "profile-mini__avatar_size_big")]/parent::a[starts-with(@href, '
                      '"/profile")]'
        )
        ADD_POST_BUTTON = (
                By.XPATH, '//div[@class="posts-container__title-area"]/button[contains(@class, "button__back")]'
                )
        POST_SUBMIT_DATA = (
                By.XPATH, '//span[text()="Создать"]/parent::button[@class="button button__back bg_button_primary btn-area__btn"]'
                )
        POST_FIELD = (
                By.XPATH, '//div[@class="post__content post-content post-content__text font_regular"]'
                )
        PROFILE_BUTTON = (
                By.XPATH, '//img[contains(@class, "profile-mini__avatar_size_big")]/parent::a[starts-with(@href, '
                '"/profile")]'
                )
        LIKE_BUTTON = (
            By.XPATH, '(//button[@class="post-action post-action__back bg_button_action"])[1]'
        )
        ACTIVE_LIKE_BUTTON = (
            By.XPATH, '//button[@class="post-action post-action__back bg_button_action post-action__back_pressed"]'
        )
        EDIT_POST_BUTTON = (
            By.XPATH, '//img[@class="button__icon"]/parent::button[@class="button button__back bg_button_icon post__header-btn"]'
        )
        DELETE_POST_BUTTON = (
            By.XPATH, '//button[@class="button button__back bg_button_error btn-area__btn"]'
        )
        NOTICE_BELL = (
            By.XPATH, '//img[@class="notice-bell__icon"]'
        )
        NOTIFICATION_FIELD = (
            By.XPATH, '//span[@class="back-notice-container__notice font_regular"]'
        )
        NOTIFICATIONS_DELETE = (
            By.XPATH,
            '//span[text()="Удалить все"]/parent::button'
        )
        NOTIFICATIONS_EMPTY_SPAN = (
            By.XPATH,
            '//span[text()="Новых уведомлений нет."]'
        )
        NOTIFICATION_OPENED = (
            By.XPATH,
            '//div[@class="sub-menu sub-menu__back bg_sub-menu sub-menu_enable"]'
        )
        FIRST_POPUP = (
            By.XPATH, '(//span[contains(@class, "notice__msg")])[1]'
        )
        COMMENT_BUTTON = (
            By.XPATH,
            '(//button[@class="post-action post-action__back bg_button_action"])[2]'
        )
        COMMENT_FIELD = (
            By.XPATH,
            '//div[@class="comment-area__input bg_input font_regular"]'
        )
        COMMENT_SEND = (
            By.XPATH,
            '//span[text()="Отправить"]'
        )
        COMMENT_TEXT = (
            By.XPATH,
            '//div[@class="comment__text font_regular"]'
        )
        COMMENT_DELETE = (
            By.XPATH,
            '//button[@class="button button__back bg_button_icon comment__edit-btn"]/img[@class="button__icon"]'
        )
        ERR_EMPTY_COMMENT = (
            By.XPATH,
            '//span[text()="Вы ввели пустой комментарий"]'
        )
        COMMENT_CROSS = (
            By.XPATH,
            '//button[@class="button button__back bg_button_icon comment__edit-btn"]'
        )

    def open(self, url=''):
        if url == '':
            self.render(self.base_url)
        else:
            self.render(url)

        self.click(self.Locators.PROFILE_BUTTON)

        self.wait(self.default_timeout).until(EC.presence_of_element_located(self.Locators.ADD_POST_BUTTON))
        self.url = self.driver.current_url

    def open_edit_page(self):
        self.open()

        self.click(self.Locators.PROFILE_EDIT_BUTTON)

        self.wait(self.default_timeout).until(EC.presence_of_element_located(self.Locators.PROFILE_EDIT_CROSS_BUTTON))

    def create_post(self, profile_page):
       profile_page.click_create_post_btn()
       post = profile_page.find(profile_page.Locators.POST_FIELD)
       post.send_keys('test')
       profile_page.click_post_submit_btn(post)

    def click_post_submit_btn(self, aPost, aTimeout=5):
       submit = self.FindIn(aPost, self.Locators.POST_SUBMIT_DATA)
       self.click_and_wait(
           submit,
           aTimeout,
           EC.none_of(
               EC.invisibility_of_element_located(self.Locators.POST_SUBMIT_DATA)
           )
       )

    def delete_post(self, limit=5):
        self.click(self.Locators.EDIT_POST_BUTTON)
        d = self.find(self.Locators.DELETE_POST_BUTTON)
        self.click_and_wait(
            d,
            limit,
            EC.invisibility_of_element_located(self.Locators.DELETE_POST_BUTTON)
        )
    
    def open_notifications(self, limit=5):
        self.click(self.Locators.NOTICE_BELL)
        b = self.find(self.Locators.NOTIFICATION_FIELD)
        self.click_and_wait(
            b,
            limit,
            EC.none_of(
            EC.invisibility_of_element_located(self.Locators.NOTIFICATION_FIELD),
            )        
        )

    def delete_notifications(self):
        self.click(self.Locators.NOTICE_BELL)
        self.click_and_wait(self.Locators.NOTIFICATIONS_DELETE, 5)

    def check_empty_notifications(self):
        return self.find(self.Locators.NOTIFICATIONS_EMPTY_SPAN)
    
    def click_create_post_btn(self):
        self.click(self.Locators.ADD_POST_BUTTON)
    
    def click_like_button(self, limit=5):
        like = self.find(self.Locators.LIKE_BUTTON)
        self.click_and_wait(
            like,
            limit,
            EC.none_of(
                EC.invisibility_of_element_located(self.Locators.ACTIVE_LIKE_BUTTON)
            )
        )

    def click_unlike_button(self, limit=5):
        unlike = self.find(self.Locators.ACTIVE_LIKE_BUTTON)
        self.click_and_wait(
            unlike,
            limit,
            EC.none_of(
            EC.invisibility_of_element_located(self.Locators.LIKE_BUTTON)
            )
        )

    def click_unlike_button(self, limit=5):
        like = self.find(self.Locators.ACTIVE_LIKE_BUTTON)
        self.click_and_wait(
            like,
            limit,
            EC.none_of(
                EC.invisibility_of_element_located(self.Locators.LIKE_BUTTON)
            )
        )

    def open_comments(self):
        self.click(self.Locators.COMMENT_BUTTON)
        self.wait().until(EC.element_to_be_clickable(self.Locators.COMMENT_SEND))

    def close_comments(self):
        self.click(self.Locators.COMMENT_BUTTON)

    def create_comment(self, hotkey=False):
        comment = self.find(self.Locators.COMMENT_FIELD)
        comment.send_keys('test')
        if hotkey:
            comment.send_keys(Keys.SHIFT, Keys.ENTER)
        else:
            send = self.find(self.Locators.COMMENT_SEND)
            self.click_and_wait(
                send, 
                5,
                EC.invisibility_of_element_located(self.Locators.COMMENT_TEXT)
            )

    def delete_comment(self):
        cross = self.find(self.Locators.COMMENT_DELETE)
        self.click_and_wait(
            cross,
            5,
            EC.invisibility_of_element_located(self.Locators.COMMENT_TEXT)
        )

    def send_empty_comment(self):
        self.click(self.Locators.COMMENT_SEND)
        self.wait().until(EC.presence_of_element_located(self.Locators.ERR_EMPTY_COMMENT))
        