# Playwright Page Object Model Framework for LeafTaps

This is a Python-based test automation framework using Playwright and the Page Object Model pattern for automating tests on the LeafTaps application.

## Features

- Page Object Model design pattern
- Cross-browser testing support (Chromium, Firefox, WebKit)
- Configurable test runs
- Detailed logging
- Test data management
- Clean, maintainable code structure

## Prerequisites

- Python 3.7+
- Node.js

## Installation

1. Clone this repository
2. Install dependencies:

```bash

pip install pytest-playwright
pip install pytest-html
pip install -r requirements.txt
playwright install
python -m pytest tests/ --browser=chromium --headed --html=report.html
pytest tests/ --mybrowser=chromium --headless=false --html=report.html --self-contained-html--force
pip install pytest-playwright pytest-html

```

## Project Structure

```
project/
├── pages/                 # Page Object classes
│   ├── base_page.py       # Base page with common methods
│   ├── login_page.py      # Login page object
│   └── ...                # Other page objects
├── tests/                 # Test scripts
│   ├── conftest.py        # Pytest configuration
│   ├── test_login.py      # Login tests
│   └── ...                # Other test modules
├── utils/                 # Utility modules
│   ├── logger.py          # Logging utility
│   └── data_helper.py     # Test data helper
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Running Tests

Run all tests:

```bash
npm test
```
Run tests in a specific browser:

```bash
npm run test:chrome
npm run test:firefox
npm run test:safari
```

Run a specific test file:

```bash
python -m pytest tests/test_login.py
```

## Configuration

You can customize test runs with these options:

```bash
python -m pytest tests/ --browser=firefox --headless=false --slow_mo=50
```

Available options:
- `--browser`: Browser to use (chromium, firefox, webkit)
- `--headless`: Run in headless mode (true/false)
- `--slow_mo`: Slow down execution speed in milliseconds

## Writing Page Objects

All page objects should inherit from `BasePage` and follow this pattern:

```python
from pages.base_page import BasePage

class ExamplePage(BasePage):
    # Selectors
    SOME_ELEMENT = "#element-id"
    
    def __init__(self, page):
        super().__init__(page)
    
    def some_action(self):
        self.click(self.SOME_ELEMENT)
```

## Writing Tests

Tests should follow this pattern:

```python
from pages.example_page import ExamplePage

class TestExample:
    def test_something(self, page):
        example_page = ExamplePage(page)
        example_page.some_action()
        assert example_page.some_validation()
```

## Test Data Management

Use the `DataHelper` class for managing test data:

```python
from utils.data_helper import DataHelper

# Generate random test data
lead_data = DataHelper.generate_test_lead_data()

# Use in tests
create_lead_page.create_new_lead(lead_data)
```