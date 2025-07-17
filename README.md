# Demo project for AI-Driven Test Automation

## Project Overview

This project explores a comprehensive framework for intelligent automation test techniques applied to a web application using Behavior-Driven Development (BDD). 
It's built with Playwright and Python, integrating with CI/CD pipelines to demonstrate robust testing capabilities across UI and API layers.

## Features

* **UI Test Automation:**
    * End-to-end testing of core e-commerce workflows.  Scenarios: User Login, Product Search, Add to Cart, Checkout Process.
    * Implemented using Playwright
* **API Test Automation:**
    * Validation of RESTful API endpoints (e.g., product retrieval).
    * Ensures data integrity and API contract adherence.
    * Implemented using Python's `requests` library.
* **Behavior-Driven Development (BDD):**
    * Tests are written in a human-readable Gherkin syntax (Given/When/Then) using Pytest-BDD.
* **Continuous Integration / Continuous Delivery (CI/CD):**
    * Automated test execution pipeline configured with GitHub Actions, triggered on every push to the `main` branch.
    * Generates comprehensive JUnit XML test results, a detailed HTML test report, and screenshots (basline, current and diff).
      
## AI-driven features
* **Intelligent Test Data Generation:**
    * Utilizes the Faker library to dynamically generate realistic test data (e.g., names, addresses) for checkout processes, reducing test data management overhead and increasing test scenario diversity.
* **Custom Visual Validation:**
    * Includes a custom image comparison solution (built with Python's Pillow library) to detect visual regressions in the UI. Automatically compares current UI screenshots against a pre-defined baseline.
* **API Schema Validation:**
    * Ensures API responses conform to a predefined JSON schema using the [jsonschema](https://python-jsonschema.readthedocs.io/) library, validating data types, structure, and required fields.

## Tech Stack

* **Language:** Python 3.9+
* **UI Automation:** Playwright
* **API Testing:** `requests` library
* **Test Framework:** Pytest
* **BDD Framework:** Pytest-BDD
* **Test Data Generation:** Faker
* **Visual Testing:** Pillow (customised function implementation)
* **Schema Validation:** jsonschema
* **CI/CD:** GitHub Actions
* **Version Control:** Git, GitHub

📁 Project Structure 
```  
├── .github/
│   └── workflows/
│       └── main.yml                # GitHub Actions CI/CD pipeline definition
├── schemas/
│   └── product_schema.json         # JSON schema for API validation
├── snapshots/                      # Stores baseline and current screenshots for visual tests
│   ├── products_page_baseline.png # Committed baseline image for comparison
│   └── products_page_current.png  # Generated during CI runs (and uploaded as artifact)
├── tests/
│   ├── api.feature                 # Gherkin feature file for API tests
│   ├── ui.feature                  # Gherkin feature file for UI tests
│   ├── steps/
│   │   ├── __init__.py             # Makes 'steps' a Python package
│   │   ├── test_api_steps.py       # Step definitions for API tests
│   │   └── test_ui_steps.py        # Step definitions for UI tests (including visual and Faker logic)
│   └── utils/
│       └── visual.py               # Reusable Python functions for visual regression tests
├── requirements.txt                # Python dependencies for local dev and CI
├── .gitignore                      # Files and folders ignored by Git
└── README.md                       # This file
```

### **CI/CD Results**

[Last GitHub Actions Run](https://github.com/onwareer/automated-testing-project/actions/runs/16344058528)

Live feedback on the build status  
[![CI](https://github.com/onwareer/automated-testing-project/actions/workflows/main.yml/badge.svg)](https://github.com/onwareer/automated-testing-project/actions/workflows/main.yml)

* **Note** API tests have been currently diabled due to a connection issue between https://fakestoreapi.com and CI environment despite running successfull in the local machine.

### 📢 Next Phases**

* **Mock API:** Implement Mock No-Hosting API setup to solve connection issue for API tests.
* **Explore Third-party tools for visual regression:** Percy (by BrowserStack) and Applitools Eyes
* **Intelligent scenarios generator:** Integrate with intelligent test scenarios generator for a more adaptive automation test framework.



