Insider Careers Automation 🚀

Automated end-to-end test framework for the Insider Careers website
 using Python + Selenium + Pytest.
The framework follows the Page Object Model (POM), is Dockerized, and ready for CI/CD (GitHub Actions + Jenkins).

📂 Project Structure
insider_automation/
│── tests/                     # Test cases
│   └── test_careers_e2e.py
│
│── pages/                     # Page Object Model classes
│   ├── base_page.py           # Shared waits, actions, helpers
│   ├── home_page.py
│   ├── careers_page.py
│   ├── qa_jobs_page.py
│   └── job_detail_page.py
│
│── utils/                     # Utilities
│   ├── logger.py
│   ├── screenshot.py
│   └── driver_factory.py
│
│── conftest.py                # Pytest fixtures
│── pytest.ini                 # Pytest configuration
│── requirements.txt           # Dependencies
│── Dockerfile                 # Docker build
│── docker-compose.yml         # Docker orchestration
│── Jenkinsfile                # Jenkins pipeline
│── Makefile                   # Shortcuts (make build/test/clean)

✨ Features

Page Object Model (POM)

Reusable waits (wait_until_visible, wait_until_clickable)

Select2 dropdown handling (robust, waits until ready)

Hover + click on job cards to reveal "View Role"

New tab switching & Lever form verification

Verify all QA jobs contain:

Position → includes "Quality Assurance"

Department → includes "Quality Assurance"

Location → includes "Istanbul, Turkey"

Error screenshots saved under utils/screenshots/error_screenshots/YYYY-MM-DD/

Logs for every step

Reports: HTML + JUnit XML

Dockerized for local/CI runs

CI/CD ready (GitHub Actions + Jenkins)

🛠️ Setup
1) Install dependencies
pip install -r requirements.txt

2) Run tests
pytest


With HTML & JUnit reports:

pytest --html=report.html --self-contained-html --junitxml=test-results.xml


Reports:

📄 report.html → detailed report

🖼️ utils/screenshots/error_screenshots/ → failure screenshots

🐳 Run with Docker
Build image
docker-compose build

Run tests
docker-compose up


Artifacts:

report.html generated in root

Screenshots stored in utils/screenshots/error_screenshots/

⚡ Run with Makefile

Build: make build

Run tests: make test

Debug container: make shell

Logs: make logs

Clean: make clean

🐙 GitHub Actions

Workflow: .github/workflows/ci.yml

Runs on push & PR

Installs Chrome + Chromedriver

Executes tests in headless mode

Uploads HTML report + screenshots as artifacts

🔧 Jenkins

Pipeline: Jenkinsfile

Runs inside Docker agent

Installs Chrome + Chromedriver

Runs pytest inside xvfb

Archives:

✅ JUnit test results (test-results.xml)

📄 HTML report (report.html)

🖼️ Screenshots

🔍 Test Scenario (E2E Flow)

Open Insider homepage

Reject cookies (English/Turkish)

Navigate: Company → Careers

Verify blocks:

Our Locations

Teams

Life at Insider

Go to QA Jobs page

Wait until filters ready

Apply filters:

Location = Istanbul, Turkey

Department = Quality Assurance

Verify all listed jobs contain:

Position → includes Quality Assurance

Department → includes Quality Assurance

Location → includes Istanbul, Turkey

Hover a job → click View Role

Switch to new tab → confirm Lever application page opened

📸 Screenshot Handling

Failures stored in:

utils/screenshots/error_screenshots/YYYY-MM-DD/


Format:

ClassName.MethodName_YYYYmmdd_HHMMSS.png

👨‍💻 Maintainer

Author: Ersin Topcu

Role: Software QA Engineer