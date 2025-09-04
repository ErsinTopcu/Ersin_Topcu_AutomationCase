from time import sleep
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CareersPage(BasePage):
    # — Blocks on the Careers site —
    LOCATIONS_BLOCK = (By.ID, "career-our-location")
    TEAMS_BLOCK = (By.ID, "career-find-our-calling")
    LIFE_AT_INSIDER_BLOCK = (
        By.XPATH,
        "//section[@data-id='a8e7b90']"
        "//h2[contains(@class,'elementor-heading-title')][normalize-space()='Life at Insider']"
    )

    # — A selector available on the QA jobs page to assert readiness —
    QA_JOB_CARDS = (By.CSS_SELECTOR, ".position-list-item")

    def verify_blocks(self):
        assert self.element_exists(self.LOCATIONS_BLOCK), "Our Locations block missing"
        assert self.element_exists(self.TEAMS_BLOCK), "Teams block missing"
        assert self.element_exists(self.LIFE_AT_INSIDER_BLOCK), "Life at Insider block missing"
        self.logger.info("Verified Careers page blocks")

    def go_to_qa(self):
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        self.logger.info("Opened Quality Assurance Job Page")