from selenium.webdriver.common.by import By


class BasePageLocators:
    NOTICE_LAST = (
        By.CSS_SELECTOR,
        'div.notice-container div.notice:nth-of-type(1) span[class~="notice__msg"]'
    )


class LoginPageLocators:
    USERNAME = (By.NAME, 'username')
    PASSWORD = (By.NAME, 'password')
    SUBMIT_BTN = (By.CSS_SELECTOR, 'form button[type="submit"]')


class ProfilePageLocators:
    ABOUT_EDIT_BTN = (
        By.CSS_SELECTOR, 'div.about__header > button'
    )
    ABOUT_CONTENT = (By.CSS_SELECTOR, 'div.about__text')
    ABOUT_CANCEL_BTN = (
        By.CSS_SELECTOR, 'form.about__form button[type="button"]'
    )
    ABOUT_SUBMIT_BTN = (
        By.CSS_SELECTOR, 'form.about__form button[type="submit"]'
    )
    POST_CREATE_BTN = (
        By.CSS_SELECTOR, 'div.posts-container__title-area button'
    )
    POST_CREATED = (
        By.XPATH,
        '//div[@class="posts-container__posts-area"]//span[text()="Создать"]/../../../../..'

    )
    POSTS_CONTAINER = (
        By.CSS_SELECTOR, 'div.posts-container__posts-area'
    )
    POST_LAST = (
        By.CSS_SELECTOR, 'div.post:last-of-type'
    )
    POST_CONTENT = (
        By.CSS_SELECTOR, 'div.post-content'
    )
    POST_LAST_CONTENT = (
        By.CSS_SELECTOR, 'div.post:last-of-type div.post-content'
    )
    POST_CANCEL_BTN = (
        By.XPATH, '//span[text()="Отмена"]/..'
    )
    POST_SUBMIT_BTN = (
        By.CSS_SELECTOR, 'button[type="submit"]'
    )
    POST_DELETE_BTN = (
        By.XPATH, '//span[text()="Удалить"]/..'
    )
    POST_LOAD_FILE = (
        By.CSS_SELECTOR, 'input[type="file"][accept*="jpg"]'
    )
    POST_IMAGES = (
        By.CSS_SELECTOR, 'img.post-content__image'
    )
    POST_SELECTOR_TIER = (
        By.CSS_SELECTOR, 'select.dropbox__select[name="tier"]'
    )
    POST_EDIT_BTN = (
        By.CSS_SELECTOR, 'div.post__header button'
    )
    POST_NOT_ALLOWED = (
        By.CSS_SELECTOR, 'div.post__not-allowed'
    )
