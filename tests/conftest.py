"""
Pytest configuration file with Playwright fixtures
"""

import os
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright, Error
from utils.logger import setup_logger

logger = setup_logger()

def pytest_addoption(parser):
    """Add custom command line options for pytest"""
    parser.addoption(
        "--mybrowser",
        action="store",
        default="chromium",
        help="Browser to run tests on: chromium, firefox, or webkit"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run tests in headless mode: true or false"
    )
    parser.addoption(
        "--slow_mo",
        action="store",
        default=0,
        type=int,
        help="Delay between operations in milliseconds"
    )

@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):
    """Fixture for browser launch settings"""
    return {
        "headless": pytestconfig.getoption("--headless").lower() == "true",
        "slow_mo": pytestconfig.getoption("--slow_mo")
    }

@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    """Fixture for browser selection"""
    return pytestconfig.getoption("--mybrowser")

@pytest.fixture(scope="session")
def browser_context_args():
    """Fixture for browser context settings"""
    video_dir = "videos"
    os.makedirs(video_dir, exist_ok=True)
    return {
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": video_dir
    }

@pytest.fixture(scope="function")
def page(request, browser_type_launch_args, browser_context_args, browser_name):
    """Playwright page fixture with trace, video, screenshot"""
    with sync_playwright() as playwright:
        browser_launcher = {
            "chromium": playwright.chromium,
            "firefox": playwright.firefox,
            "webkit": playwright.webkit
        }.get(browser_name, playwright.chromium)

        browser = browser_launcher.launch(**browser_type_launch_args)
        context = browser.new_context(**browser_context_args)
        page = context.new_page()

        # Trace start
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.on("console", lambda msg: logger.warning(f"Console {msg.type}: {msg.text}")
                if msg.type == "error" else None)
        logger.info(f"Starting test with {browser_name} browser")

        yield page

        # Trace stop
        test_name = request.node.name
        trace_path = f"traces/{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        os.makedirs(os.path.dirname(trace_path), exist_ok=True)
        context.tracing.stop(path=trace_path)

        # Screenshot on failure
        if request.node.rep_call.failed:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
            page.screenshot(path=screenshot_path, full_page=True)
            logger.error(f"Test failed. Screenshot saved to: {screenshot_path}")
            if hasattr(request.node, "add_report_section"):
                request.node.add_report_section("call", "screenshot", f"file://{screenshot_path}")

        # Close
        context.close()
        browser.close()
        logger.info("Closed browser after test")

# For HTML report integration (pytest-html)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Give control to pytest to get the report object
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    # Attach screenshot if failed and html report is active
    if rep.when == "call" and rep.failed:
        screenshot_path = f"screenshots/{item.name}.png"
        if os.path.exists(screenshot_path):
            extra = getattr(rep, "extra", [])
            html = f'<div><img src="{screenshot_path}" alt="screenshot" style="width:400px;" onclick="window.open(this.src)" /></div>'
            extra.append(pytest_html.extras.html(html))
            rep.extra = extra

@pytest.fixture(scope="function")
def test_data():
    """Static test data used across test cases"""
    return {
        "valid_user": {
            "username": "DemoSalesManager",
            "password": "crmsfa"
        },
        "invalid_user": {
            "username": "invalid",
            "password": "invalid"
        }
    }
