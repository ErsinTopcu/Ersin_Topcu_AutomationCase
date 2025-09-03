from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    COMPANY_MENU = (By.XPATH, "//a[contains(@class,'dropdown-toggle') and normalize-space(text())='Company']")
    CAREERS = (By.XPATH, "//a[@class='dropdown-sub' and normalize-space(text())='Careers']")
    COOKIE_REJECT = (By.XPATH, "//a[@id='wt-cli-reject-btn']")

    def open(self):
        self.driver.get("https://useinsider.com/")
        self.logger.info("Opened Insider homepage")

    def reject_cookies(self):
        if self.element_exists(self.COOKIE_REJECT):
            self.click(self.COOKIE_REJECT)
            self.logger.info("Cookie banner rejected")

    def go_to_careers(self):
        self.click(self.COMPANY_MENU)
        self.click(self.CAREERS)
        self.logger.info("Navigated to Careers page")
