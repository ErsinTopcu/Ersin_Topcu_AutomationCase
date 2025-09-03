# Ersin_Topcu_AutomationCase

This repository contains an **end-to-end Selenium Test Automation Framework** built with Python, following the **Page Object Model (POM)** design pattern.  
It is designed to be modular, maintainable, and easily integrated into CI/CD pipelines.

---

## 🚀 Features
- **Page Object Model (POM)** for modular and reusable test code  
- **Explicit Waits** (`WebDriverWait` + Expected Conditions)  
- **Logging Helper** – All test steps are logged and visible in the console  
- **Smart Scroll** – Automatically scrolls until lazy-loaded elements are visible  
- **Automatic Screenshots on Failures** – Stored in date-based folders  
- **Cookie Banner Handling** – Rejects cookie banners (supports TR & EN)  
- **CI/CD Ready** – Can be easily integrated into Jenkins, GitHub Actions, GitLab CI etc.  
- **Cross-browser Support** – Easily extendable to Chrome, Firefox, Edge  

---

## 📂 Project Structure
```
Ersin_Topcu_AutomationCase/
│
├── pages/                       # Page Object classes
│   ├── base_page.py              # BasePage with common methods
│   ├── home_page.py              # Home Page elements & actions
│   ├── careers_page.py           # Careers Page elements & actions
│   ├── job_detail_page.py        # Job Detail Page elements & actions
│   └── qa_jobs_page.py           # QA Jobs Page elements & actions
│
├── tests/                       
│   └── test_careers_e2e.py       # E2E flow test for Careers -> QA Jobs
│
├── utils/                       
│   ├── driver_factory.py         # Driver setup (Chrome, Firefox, etc.)
│   ├── logger.py                 # Logger configuration
│   └── screenshots/              # Stores screenshots on failures
│
├── .venv/                        # Virtual environment (ignored in VCS)
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 🔧 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Ersin_Topcu_AutomationCase.git
cd Ersin_Topcu_AutomationCase
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate the Environment
- **Windows (PowerShell)**
```bash
.venv\Scripts\activate
```
- **Linux / Mac**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧪 Running the Tests

### Run all tests
```bash
pytest -v
```

### Run with HTML report
```bash
pytest --html=report.html --self-contained-html
```

### Run a specific test
```bash
pytest tests/test_careers_e2e.py -v
```

---

## 📸 Screenshots
- When a test fails, a screenshot is automatically saved under:
```
utils/screenshots/<YYYY-MM-DD>/<test_name>.png
```

---

## 🧩 Example End-to-End Flow
The sample E2E test (`test_careers_e2e.py`) validates:

1. Navigate to **Home Page**  
2. Reject cookie banner  
3. Open **Company → Careers** menu  
4. Filter job positions by **Quality Assurance**  
5. Select location (e.g., **Istanbul, Turkiye**)  
6. Click **See all QA jobs**  
7. Verify job details (title, department, location, etc.)  

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+  
- **Framework:** PyTest  
- **UI Automation:** Selenium WebDriver  
- **Design Pattern:** Page Object Model (POM)  
- **Logging:** Python Logging Module  
- **Reporting:** Pytest-HTML  

---

## 📜 License
This project is licensed under the MIT License.

---

# 📦 requirements.txt
```
selenium>=4.18.1
webdriver-manager>=4.0.1
pytest>=8.0.0
pytest-html>=4.1.1
```
