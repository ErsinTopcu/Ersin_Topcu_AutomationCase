# Insider Careers Automation 🚀

Automated **end-to-end test framework** for the [Insider Careers website](https://useinsider.com/careers/quality-assurance/) using **Python + Selenium + Pytest**.  
The framework follows the **Page Object Model (POM)**, is **Dockerized**, and ready for **CI/CD** (GitHub Actions + Jenkins).  

---

## 📂 Project Structure

```
├── pages/                   # Page Object classes (POM)
│   ├── base_page.py         # Shared waits, actions, helpers
│   ├── home_page.py
│   ├── careers_page.py
│   ├── qa_jobs_page.py
│   └── job_detail_page.py
├── tests/
│   └── test_careers_e2e.py  # Main E2E scenario
├── utils/                   # Logger, screenshots, driver factory
│   ├── driver_factory.py
│   ├── logger.py
│   └── screenshot.py
├── .github/workflows/ci.yml # GitHub Actions (CI)
├── conftest.py              # Pytest fixtures
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container image
├── Jenkinsfile              # Jenkins pipeline
├── Makefile                 # make build/test/clean helpers
├── pytest.ini               # Pytest config
├── requirements.txt         # Dependencies
└── README.md
```

---

## ✨ Features

- 🧩 Modular **Page Object Model (POM)** architecture (clear page responsibilities)
- ⏱️ Explicit synchronization via **WebDriverWait** + **Expected Conditions**
- 🧭 Readiness utilities: **DOM complete** check, **smart scroll**, presence/visibility/clickable helpers
- 🔽 **Select2-capable** dropdown utilities (search-first with robust fallbacks)
- ♻️ **Lazy-load aware** scrolling to stabilize infinite lists
- 🪟 New tab/window switching with **URL substring** assertion
- 🧾 Structured, readable **logging** for step-by-step traceability
- 📸 **Automatic screenshots** on failures (dated directories)
- 🍪 Cookie banner handling (multi-locale ready)
- 🧪 **Pytest-first** setup with fixtures and configuration
- ⚙️ **CI/CD-friendly**: headless execution, report & artifact hooks

---

## 🛠️ Setup

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Run tests
```bash
pytest
```

With HTML & JUnit reports:
```bash
pytest --html=report.html --self-contained-html --junitxml=test-results.xml
```

Reports:
- 📄 `report.html` → detailed report  
- 🖼️ `utils/screenshots/error_screenshots/` → failure screenshots  

---

## 🐳 Run with Docker

### Build image
```bash
docker-compose build
```

### Run tests
```bash
docker-compose up
```

Artifacts:
- `report.html` generated in root  
- Screenshots stored in `utils/screenshots/error_screenshots/`  

---

## ⚡ Run with Makefile

- Build: `make build`  
- Run tests: `make test`  
- Debug container: `make shell`  
- Logs: `make logs`  
- Clean: `make clean`  

---

## 🐙 GitHub Actions

Workflow: `.github/workflows/ci.yml`  
- Runs on **push & PR**  
- Installs Chrome + Chromedriver  
- Executes tests in headless mode  
- Uploads **HTML report** + **screenshots** as artifacts  

---

## 🔧 Jenkins

Pipeline: `Jenkinsfile`  
- Runs inside Docker agent  
- Installs Chrome + Chromedriver  
- Runs `pytest` inside `xvfb`  
- Archives:
  - ✅ JUnit test results (`test-results.xml`)  
  - 📄 HTML report (`report.html`)  
  - 🖼️ Screenshots  

---

## 🔍 Test Scenario (E2E Flow)

1. Open Insider homepage  
2. Reject cookies (English/Turkish)  
3. Navigate: **Company → Careers**  
4. Verify blocks:
   - *Our Locations*  
   - *Teams*  
   - *Life at Insider*  
5. Go to **QA Jobs page**  
6. Wait until **filters ready**  
7. Apply filters:
   - Location = *Istanbul, Turkey*  
   - Department = *Quality Assurance*  
8. Verify all listed jobs contain:
   - Position → includes *Quality Assurance*  
   - Department → includes *Quality Assurance*  
   - Location → includes *Istanbul, Turkey*  
9. Hover a job → click **View Role**  
10. Switch to new tab → confirm **Lever application page** opened  

---

## 📸 Screenshot Handling

- Failures stored in:
  ```
  utils/screenshots/error_screenshots/YYYY-MM-DD/
  ```
- Format:
  ```
  ClassName.MethodName_YYYYmmdd_HHMMSS.png
  ```

---

## 👨‍💻 Maintainer

- **Author:** Ersin Topcu  
- **Role:** Software QA Engineer  
