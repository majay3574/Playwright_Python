"""
Pytest configuration file with Playwright fixtures, Allure & HTML reporting
"""

import configparser
import os
import pytest
import allure
from allure_commons.types import AttachmentType
from datetime import datetime
from playwright.sync_api import sync_playwright
import pytest_html
from utils.logger import setup_logger
from data.user_credentials import valid_user, invalid_user

logger = setup_logger()

def pytest_addoption(parser):
    """Add custom command line options for pytest"""
    parser.addoption("--mybrowser", action="store", default="chromium", help="Browser to run tests on")
    parser.addoption("--headless", action="store", default="false", help="Run tests in headless mode")
    parser.addoption("--slow_mo", action="store", default=0, type=int, help="Delay between operations in ms")

@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):
    return {
        "headless": pytestconfig.getoption("--headless").lower() == "true",
        "slow_mo": pytestconfig.getoption("--slow_mo")
    }

@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("--mybrowser")

@pytest.fixture(scope="session")
def browser_context_args():
    video_dir = "videos"
    os.makedirs(video_dir, exist_ok=True)
    return {
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": video_dir
    }

@pytest.fixture(scope="function")
def page(request, browser_type_launch_args, browser_context_args):
    config = configparser.ConfigParser()
    config.read("config.properties")

    browser_name = config.get("default", "browser", fallback="chromium").lower()
    trace_dir = config.get("default", "trace.dir", fallback="traces")

    os.makedirs(trace_dir, exist_ok=True)

    with sync_playwright() as playwright:
        if browser_name == "chrome":
            browser_type = playwright.chromium
            launch_args = {"channel": "chrome", **browser_type_launch_args}
        elif browser_name == "msedge":
            browser_type = playwright.chromium
            launch_args = {"channel": "msedge", **browser_type_launch_args}
        elif browser_name == "firefox":
            browser_type = playwright.firefox
            launch_args = browser_type_launch_args
        elif browser_name == "webkit":
            browser_type = playwright.webkit
            launch_args = browser_type_launch_args
        else:
            browser_type = playwright.chromium
            launch_args = browser_type_launch_args

        browser = browser_type.launch(**launch_args)
        context = browser.new_context(**browser_context_args)
        page = context.new_page()

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.on("console", lambda msg: logger.warning(f"Console {msg.type}: {msg.text}")
                if msg.type == "error" else None)
        logger.info(f"Starting test with {browser_name} browser")

        with allure.step(f"Launch {browser_name} browser and open new page"):
            yield page

        test_name = request.node.name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        trace_path = os.path.join(trace_dir, f"{test_name}_{timestamp}.zip")
        context.tracing.stop(path=trace_path)

        if os.path.exists(trace_path):
            allure.attach.file(
                trace_path,
                name="Playwright Trace",
                attachment_type="application/zip"
            )

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
                attachment_type=AttachmentType.PNG
            )

        try:
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
                    attachment_type=AttachmentType.WEBM
                )
        except Exception as e:
            logger.error(f"Failed to attach video: {e}")
            try:
                context.close()
                browser.close()
            except:
                pass

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
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

@pytest.fixture(scope="function")
def test_data():
    return {
        "valid_user": valid_user,
        "invalid_user": invalid_user
    }
