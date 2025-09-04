from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

class QaJobsPage(BasePage):
    # --- Filters (Select2 containers) ---
    FILTER_LOCATION = (By.ID, "select2-filter-by-location-container")
    FILTER_DEPARTMENT = (By.ID, "select2-filter-by-department-container")

    # Select2 results container appears as a separate dropdown
    # We'll target options by visible text.
    SELECT2_DROPDOWN = (By.CSS_SELECTOR, "ul.select2-results__options")


    # --- Results / jobs list ---
    JOBS_CARD = (By.ID, "jobs-list")
    FIRST_VIEW_ROLE = (By.XPATH, "(//a[contains(text(),'View Role')])[1]")

    def wait_until_filters_ready(self, timeout: int = 20):
        """Ensure QA jobs page and both Select2 triggers are ready before clicking."""
        # page readyState
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        # both filters visible & clickable
        filters = [self.FILTER_LOCATION, self.FILTER_DEPARTMENT]
        combined_locator = (
            By.CSS_SELECTOR,
            "#select2-filter-by-location-container, #select2-filter-by-department-container",
        )
        wait.until(EC.visibility_of_all_elements_located(combined_locator))
        for locator in filters:
            wait.until(EC.element_to_be_clickable(locator))
        self.logger.info("QA Jobs page & filters are ready.")


    def verify_jobs_loaded(self):
        """Wait until at least one job card is present, then return the list."""
        self.logger.info("Waiting for job cards to load...")
        self.wait.until(EC.presence_of_element_located(self.JOBS_CARD))
        cards = self.driver.find_elements(*self.JOBS_CARD)
        self.logger.info(f"Total {len(cards)} job cards found.")
        return cards

    def _open_select2_dropdown(self, trigger_locator, tries: int = 2):
        """Open Select2 dropdown with safe click; retry with JS if needed."""
        last_err = None
        for attempt in range(1, tries + 1):
            try:
                trigger = self.wait_until_clickable(trigger_locator, "Select2 trigger not clickable")
                trigger.click()
                # dropdown visible?
                self.wait_until_visible(self.SELECT2_DROPDOWN, "Select2 results not visible")
                return
            except Exception as e:
                last_err = e
                # try JS click fallback
                try:
                    el = self.wait_until_visible(trigger_locator)
                    self.driver.execute_script("arguments[0].click();", el)
                    self.wait_until_visible(self.SELECT2_DROPDOWN, "Select2 results not visible")
                    return
                except Exception as inner:
                    last_err = inner
        # if reached here, open failed
        raise last_err
    def _select_from_select2(self, container_locator, option_text: str):
        """
        Click the Select2 trigger, wait for dropdown, select by exact visible text.
        No scroll, no typing; pure dropdown pick.
        """
        # open dropdown robustly
        self._open_select2_dropdown(container_locator)

        # pick option
        option_locator = (
            By.XPATH,
            "//ul[contains(@class,'select2-results__options')]"
            f"//li[contains(@class,'select2-results__option')][normalize-space()='{option_text}']"
        )
        self.wait_until_clickable(option_locator, f"Option '{option_text}' not clickable").click()

        # wait dropdown closes
        self.wait.until(EC.invisibility_of_element_located(self.SELECT2_DROPDOWN))
        self.logger.info(f"Selected '{option_text}' from Select2")

    def filter_jobs(self, location_text: str = "Istanbul, Turkey", department_text: str = "Quality Assurance"):
        """Apply filters: Location + Department using Select2 dropdowns."""
        # PRECONDITION: call wait_until_filters_ready() before this
        self._select_from_select2(self.FILTER_LOCATION, location_text)
        self._select_from_select2(self.FILTER_DEPARTMENT, department_text)
        self.logger.info(f"Applied filters -> Location: '{location_text}', Department: '{department_text}'")


    def open_job_by_index_via_hover(self, index: int = 0):
        """Hover over a job card to reveal 'View Role' button, then click it."""
        cards = self.driver.find_elements(*self.JOB_CARD)
        assert cards, "No job cards found"
        assert index < len(cards), f"Index {index} out of range; only {len(cards)} jobs"

        card = cards[index]
        self.logger.info(f"Hovering job card at index {index}")

        # Hover over the card to reveal the button
        ActionChains(self.driver).move_to_element(card).perform()

        # Find 'View Role' button inside this card (relative XPath)
        view_role_btn = card.find_element(By.XPATH, ".//a[contains(., 'View Role')]")

        # Ensure it's clickable now that we've hovered
        self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//a[contains(., 'View Role')]")))
        view_role_btn.click()
        self.logger.info("Clicked 'View Role' on hovered job card")
