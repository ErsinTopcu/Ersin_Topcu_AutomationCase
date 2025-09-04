from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class QaJobsPage(BasePage):
    # — Filters (Select2 triggers) —
    FILTER_LOCATION   = (By.ID, "select2-filter-by-location-container")
    FILTER_DEPARTMENT = (By.ID, "select2-filter-by-department-container")

    # — Select2 results UL —
    SELECT2_RESULTS_UL = (By.CLASS_NAME, "select2-results__options")

    # — Jobs list —
    JOB_CARDS = (By.CSS_SELECTOR, ".position-list-item")
    RESULT_COUNTER = (By.ID, "resultCounter")

    # — “View Role” shortcut —
    FIRST_VIEW_ROLE = (By.XPATH, "(//a[contains(text(),'View Role')])[1]")

    # — Navigate to QA open positions listing —
    QA_JOBS_LINK = (By.XPATH, "//a[contains(@href, '/careers/open-positions/') and normalize-space()='See all QA jobs']")

    def go_to_qa_jobs(self):
        """
        Click the 'See all QA jobs' → assert landing on the expected open positions page
        (via URL contains check) → verify the page is fully loaded, and ensure the
        Department dropdown value is 'Quality Assurance'.
        """

        # Click the 'See all QA jobs'
        self.click(self.QA_JOBS_LINK)
        self.logger.info("Clicked 'See all QA jobs' CTA")

        # Wait for the URL to change
        self.wait.until(EC.url_contains("/careers/open-positions/?department=qualityassurance"))

        # Ensure the DOM is fully loaded
        self.wait_dom_complete()

        # Scroll to the bottom until lazy-load is complete
        self.scroll_to_bottom_until_stable()

        # Verify job cards are actually present
        cards = self.wait_until_any_present(self.JOB_CARDS, "QA jobs page did not load job cards")
        assert len(cards) > 0, "QA jobs page job card container is present but empty"
        self.logger.info(f"Initial job cards present: {len(cards)}")

        # Ensure resultCounter is visible
        self.smart_scroll(self.RESULT_COUNTER)
        self.wait_until_visible(self.RESULT_COUNTER, "resultCounter not visible after scroll back")
        self.logger.info("resultCounter is visible after bottom-scroll cycle")

        # Verify that filter triggers are clickable
        self.wait_until_clickable(self.FILTER_LOCATION, "Location filter not clickable")
        self.wait_until_clickable(self.FILTER_DEPARTMENT, "Department filter not clickable")
        self.logger.info("Filter triggers are clickable — page fully ready")

        # Ensure the Department dropdown value is 'Quality Assurance' ---
        self.smart_scroll(self.FILTER_DEPARTMENT)
        self.wait_until_visible(self.FILTER_DEPARTMENT, "Department filter container not visible")

        # Wait until the text appears inside the container
        self.wait.until(EC.text_to_be_present_in_element(self.FILTER_DEPARTMENT, "Quality Assurance"))

        # Double-check by reading the element's text (fallback to 'title' if needed)
        dept_el = self.driver.find_element(*self.FILTER_DEPARTMENT)
        raw_text = (dept_el.text or dept_el.get_attribute("title") or "").strip()
        normalized = " ".join(raw_text.replace("×", "").split())

        assert normalized == "Quality Assurance", (
            f"Unexpected department value: raw={raw_text!r} → normalized={normalized!r}"
        )
        self.logger.info("Department dropdown value asserted: 'Quality Assurance'")

    def filter_jobs(
        self,
        location_text: str = "Istanbul, Turkiye",
        department_text: str = "Quality Assurance"
    ):
        """
        Assumes CareersPage.go_to_qa_jobs() already ensured the page is fully ready.
        1) Location: open dropdown -> scroll inside UL until option visible -> click
        2) Department: same flow
        """
        self._select_from_select2_with_ul_scroll(self.FILTER_LOCATION, location_text)
        self._select_from_select2_with_ul_scroll(self.FILTER_DEPARTMENT, department_text)
        self.logger.info(f"Applied filters -> Location: '{location_text}', Department: '{department_text}'")

    def verify_jobs_loaded(self):
        """Ensure at least one job card exists after filtering."""
        self.logger.info("Verifying job cards exist after filtering...")
        cards = self.wait_until_any_present(self.JOB_CARDS, "Job cards not present after filtering")
        assert len(cards) > 0, "No job cards found after filtering"
        self.logger.info(f"Job cards count after filtering: {len(cards)}")
        return cards

    def open_job_by_index_via_hover(self, index: int = 0):
        """Hover over a job card to reveal 'View Role' button, then click it."""
        cards = self.driver.find_elements(*self.JOB_CARDS)
        assert cards, "No job cards found"
        assert index < len(cards), f"Index {index} out of range; only {len(cards)} jobs"

        card = cards[index]
        self.logger.info(f"Hovering job card at index {index}")
        ActionChains(self.driver).move_to_element(card).perform()

        view_role_btn = card.find_element(By.XPATH, ".//a[contains(., 'View Role')]")
        self.wait.until(lambda d: view_role_btn.is_displayed() and view_role_btn.is_enabled())
        view_role_btn.click()
        self.logger.info("Clicked 'View Role' on hovered job card")

    # ---------- Private helpers ----------

    def _select_from_select2_with_ul_scroll(self, trigger_locator, option_text: str, step_px: int = 260, max_steps: int = 15):
        """Open Select2, ensure the UL is visible, scroll the UL until the target text is visible, then click."""
        self.wait_until_clickable(trigger_locator, "Select2 trigger not clickable").click()
        ul_el = self.wait_until_visible(self.SELECT2_RESULTS_UL, "Select2 results UL not visible")

        option_xpath = ".//li[contains(@class,'select2-results__option')][normalize-space()='{text}']".format(
            text=option_text
        )

        for _ in range(max_steps):
            matches = ul_el.find_elements(By.XPATH, option_xpath)
            if matches:
                target = matches[0]
                ActionChains(self.driver).move_to_element(target).pause(0.1).perform()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath))).click()
                self.wait.until(EC.invisibility_of_element_located(self.SELECT2_RESULTS_UL))
                self.logger.info(f"Selected '{option_text}' from Select2")
                return

            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[1];",
                ul_el, step_px
            )
            sleep(0.1)

        raise AssertionError(f"Option '{option_text}' not found in Select2 after {max_steps} steps")
