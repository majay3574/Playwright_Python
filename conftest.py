"""
Pytest configuration file with Playwright fixtures, Allure & HTML reporting
"""

import os
import pytest
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright
import pytest_html
from utils.logger import setup_logger
from data.user_credentials import valid_user, invalid_user

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
    """Playwright page fixture with tracing, video, screenshot, and Allure reporting"""
    with sync_playwright() as playwright:
        browser_launcher = {
            "chromium": playwright.chromium,
            "firefox": playwright.firefox,
            "webkit": playwright.webkit
        }.get(browser_name, playwright.chromium)

        browser = browser_launcher.launch(**browser_type_launch_args)
        context = browser.new_context(**browser_context_args)
        page = context.new_page()

        # Start tracing
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        # Capture console errors and log
        page.on("console", lambda msg: logger.warning(f"Console {msg.type}: {msg.text}")
                if msg.type == "error" else None)
        logger.info(f"Starting test with {browser_name} browser")

        with allure.step(f"Launch {browser_name} browser and open new page"):
            yield page

        # After test execution:

        # Stop tracing and save
        test_name = request.node.name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        trace_dir = "traces"
        os.makedirs(trace_dir, exist_ok=True)
        trace_path = os.path.join(trace_dir, f"{test_name}_{timestamp}.zip")
        context.tracing.stop(path=trace_path)

        # Attach trace to Allure
        if os.path.exists(trace_path):
            allure.attach.file(
                trace_path,
                name="Playwright Trace",
                attachment_type=allure.attachment_type.ZIP
            )

        # Screenshot on failure
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
            page.screenshot(path=screenshot_path, full_page=True)

            logger.error(f"Test failed. Screenshot saved to: {screenshot_path}")

            if hasattr(request.node, "add_report_section"):
                request.node.add_report_section("call", "screenshot", f"file://{screenshot_path}")

            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

        # Attach video to Allure
        try:
            # Close page first to finalize video file
            page.close()
            video_path = None
            if page.video:
                video_path = page.video.path()

            context.close()
            browser.close()

            if video_path and os.path.exists(video_path):
                allure.attach.file(
                    video_path,
                    name="Execution Video",
                    attachment_type=allure.attachment_type.WEBM
                )
        except Exception as e:
            logger.error(f"Failed to attach video: {e}")
            # Make sure to close context/browser even on error
            try:
                context.close()
                browser.close()
            except:
                pass

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to attach screenshots to pytest-html on test failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        screenshot_path = f"screenshots/{item.name}.png"
        if os.path.exists(screenshot_path):
            extra = getattr(rep, "extra", [])
            html = f'<div><img src="{screenshot_path}" alt="screenshot" style="width:400px;" onclick="window.open(this.src)" /></div>'
            extra.append(pytest_html.extras.html(html))
            rep.extra = extra

# @pytest.fixture(scope="function")
# def test_data():
#     """Static test data used across test cases"""
#     return {
#         "valid_user": {
#             "username": "DemoSalesManager",
#             "password": "crmsfa"
#         },
#         "invalid_user": {
#             "username": "invalid",
#             "password": "invalid"
#         }
#     }



@pytest.fixture(scope="function")
def test_data():
    """Static test data used across test cases"""
    return {
        "valid_user": valid_user,
        "invalid_user": invalid_user
    }