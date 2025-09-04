from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_jobs_page import QaJobsPage
from pages.job_detail_page import JobDetailPage
from utils.screenshot import take_screenshot

class TestCareersE2E:
    def test_careers_flow(self, driver):
        home = HomePage(driver)
        careers = CareersPage(driver)
        qa_jobs = QaJobsPage(driver)
        job_detail = JobDetailPage(driver)

        try:
            home.open()
            home.reject_cookies()
            home.go_to_careers()

            careers.verify_blocks()
            careers.go_to_qa()
            qa_jobs.go_to_qa_jobs()

            qa_jobs.filter_jobs(location_text="Istanbul, Turkiye", department_text="Quality Assurance")
            qa_jobs.verify_jobs_loaded()
            job_detail.verify_all_job_details()
            qa_jobs.open_job_by_index_via_hover()
            home.switch_to_new_tab_and_verify("https://jobs.lever.co/useinsider", timeout=10)

        except Exception as e:
            take_screenshot(driver, self.__class__.__name__, "test_careers_flow")
            raise e
