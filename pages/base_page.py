from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = get_logger()

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self.logger.info(f"Clicked element: {locator}")

    def type(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
        self.logger.info(f"Typed '{text}' into element: {locator}")

    def element_exists(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def smart_scroll(self, locator):
        """Your existing smart_scroll; keep as-is if already implemented."""
        el = self.wait_until_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        return el

    # --- Generic waits ---
    def wait_until_visible(self, locator, message: str = ""):
        return self.wait.until(EC.visibility_of_element_located(locator), message)

    def wait_until_clickable(self, locator, message: str = ""):
        return self.wait.until(EC.element_to_be_clickable(locator), message)

    def wait_until_any_present(self, locator, message: str = ""):
        self.wait.until(EC.presence_of_element_located(locator), message)
        return self.driver.find_elements(*locator)

    def wait_dom_complete(self, timeout: int = 20):
        """Wait until document.readyState == 'complete'."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def switch_to_new_tab_and_verify(self, expected_url_contains: str, timeout: int = 10):
        """
        Switch to the newly opened tab and verify the URL contains the expected substring.
        Call this right after the click that opens the new tab.
        """
        from selenium.webdriver.support.ui import WebDriverWait

        # Wait until a second tab exists
        WebDriverWait(self.driver, timeout).until(lambda d: len(d.window_handles) > 1)

        # Switch to the last handle (newly opened tab)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Verify URL contains expected substring
        WebDriverWait(self.driver, timeout).until(lambda d: expected_url_contains in d.current_url)
        current = self.driver.current_url
        assert expected_url_contains in current, f"New tab URL mismatch. Expected contains: {expected_url_contains}, got: {current}"
        return current

    def scroll_to_bottom_until_stable(self, max_passes: int = 8, settle_checks: int = 2, sleep_s: float = 0.3):
        """
        Repeatedly scroll to the bottom until page height stops growing
        for 'settle_checks' consecutive iterations (handles lazy-loading).
        """
        stable = 0
        last_h = 0
        for _ in range(max_passes):
            h = self.driver.execute_script("return document.body.scrollHeight")
            if h == last_h:
                stable += 1
                if stable >= settle_checks:
                    break
            else:
                stable = 0
                last_h = h
            self.driver.execute_script("window.scrollTo(0, arguments[0]);", h)
            sleep(sleep_s)