from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class Redirect:
    def redirected(page : BasePage, timeout = 5):
        page.wait(timeout).until(EC.url_changes(page.url))
    
    def not_redirected(page : BasePage, timeout = 5):
        page.wait(timeout).until(EC.url_to_be(page.url))

