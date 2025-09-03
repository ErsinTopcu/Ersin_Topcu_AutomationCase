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

    def get_text(self, locator):
        text = self.wait.until(EC.visibility_of_element_located(locator)).text
        self.logger.info(f"Got text from {locator}: {text}")
        return text

    def element_exists(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def smart_scroll(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled to element: {locator}")

    def wait_until_visible(self, locator, message: str = ""):
        return self.wait.until(EC.visibility_of_element_located(locator), message)

    def wait_until_clickable(self, locator, message: str = ""):
        return self.wait.until(EC.element_to_be_clickable(locator), message)

    def switch_to_new_tab_and_verify(self, expected_url_contains: str, timeout: int = 15):
        """Wait for a new tab, switch to it, then verify URL contains substring."""
        original_handles = self.driver.window_handles
        self.logger.info(f"Current window handles before click: {original_handles}")

        # Wait until a new window/tab is opened
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > len(original_handles)
        )

        new_handles = self.driver.window_handles
        self.logger.info(f"New window handles after click: {new_handles}")

        # Switch to the newest handle
        new_tab = [h for h in new_handles if h not in original_handles][0]
        self.driver.switch_to.window(new_tab)

        # Verify expected URL part
        WebDriverWait(self.driver, timeout).until(
            lambda d: expected_url_contains in d.current_url
        )
        self.logger.info(f"Switched to new tab with URL: {self.driver.current_url}")