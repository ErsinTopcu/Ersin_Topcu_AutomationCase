from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class JobDetailPage(BasePage):
    JOB_POSITIONS = (By.CSS_SELECTOR, ".position-title")
    JOB_DEPARTMENTS = (By.CSS_SELECTOR, ".position-department")
    JOB_LOCATIONS = (By.CSS_SELECTOR, ".position-location")

    def verify_all_job_details(self):
        positions = self.driver.find_elements(*self.JOB_POSITIONS)
        departments = self.driver.find_elements(*self.JOB_DEPARTMENTS)
        locations = self.driver.find_elements(*self.JOB_LOCATIONS)

        assert positions, "No job positions found"
        assert departments, "No job departments found"
        assert locations, "No job locations found"

        for idx, (pos, dept, loc) in enumerate(zip(positions, departments, locations), start=1):
            pos_text = pos.text.strip()
            dept_text = dept.text.strip()
            loc_text = loc.text.strip()

            assert "Quality Assurance" in pos_text, f"Position missing 'Quality Assurance' in job {idx}: {pos_text}"
            assert "Quality Assurance" in dept_text, f"Department mismatch in job {idx}: {dept_text}"
            assert "Istanbul, Turkey" in loc_text, f"Location mismatch in job {idx}: {loc_text}"

            self.logger.info(
                f"Job {idx} verified → Position: {pos_text}, Department: {dept_text}, Location: {loc_text}"
            )