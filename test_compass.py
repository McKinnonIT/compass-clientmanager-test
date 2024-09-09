import json
import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect, sync_playwright

load_dotenv()

COOKIE_FILE = os.getenv("SESSIONID_COOKIE_FILE")


def post_request_authenticated(page):
    """Perform a POST request using the authenticated session."""
    response = page.request.post(
        "https://mckinnonsc-vic.compass.education/Services/Configure.svc/GetAllClients",
        headers={"Content-Type": "application/json"},
    )

    if response.ok:
        print("POST request was successful.")
        print(f"Response status: {response.status}")
        print(f"Response body: {response.text()}")
    else:
        print(f"POST request failed with status: {response.status}")


def save_aspnet_sessionid(context):
    """Save only the ASP.NET_SessionId cookie to a file."""
    cookies = context.cookies()
    aspnet_cookie = [
        cookie for cookie in cookies if cookie["name"] == "ASP.NET_SessionId"
    ]

    if aspnet_cookie:
        os.makedirs(os.path.dirname(COOKIE_FILE), exist_ok=True)
        with open(COOKIE_FILE, "w") as f:
            json.dump(aspnet_cookie, f)
        print(f"ASP.NET_SessionId cookie saved to {COOKIE_FILE}")
    else:
        print("ASP.NET_SessionId cookie not found.")


def load_aspnet_sessionid(context):
    """Load the ASP.NET_SessionId cookie from a file into the browser context."""
    try:
        with open(COOKIE_FILE, "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print(f"ASP.NET_SessionId cookie loaded from {COOKIE_FILE}")
    except FileNotFoundError:
        print("No ASP.NET_SessionId cookie found, starting fresh.")


@pytest.fixture(scope="session")
def playwright():
    """Set up Playwright."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright):
    """Set up a new browser instance."""
    browser = playwright.firefox.launch(
        headless=False
    )  # You can use headless=True if you don't want the browser to be visible.
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def context(browser):
    """Set up a new browser context and load ASP.NET_SessionId cookie if it exists."""
    context = browser.new_context()
    load_aspnet_sessionid(context)
    yield context
    context.close()


@pytest.fixture(scope="session")
def page(context):
    """Create a new page for testing."""
    page = context.new_page()
    yield page
    page.close()


def test_login(page: Page):
    """Test that logs in and saves the ASP.NET_SessionId cookie."""
    page.goto("https://mckinnonsc-vic.compass.education/")

    page.get_by_placeholder("Username").fill(os.getenv("COMPASS_USER"))
    page.get_by_placeholder("Password").fill(os.getenv("COMPASS_PASS"))
    page.locator('[data-test="sign-in-submit-button"]').click()

    # Save only the ASP.NET_SessionId cookie after successful login
    save_aspnet_sessionid(page.context)

    expect(page.get_by_label("User Profile")).to_be_visible()


def test_logged_in_with_sessionid(page):
    """Test that reuses the ASP.NET_SessionId cookie to stay logged in."""
    page.goto("https://mckinnonsc-vic.compass.education/")

    # Check for an element visible only when logged in
    expect(page.get_by_label("User Profile")).to_be_visible()


def test_check_client_error_in_c_main(page: Page):
    """Test to check if any elements on the page contain the .client-error class and fail if found."""

    page.goto(
        "https://mckinnonsc-vic.compass.education/Configure/ConnectedClients.aspx"
    )

    page.get_by_text("Client Type: CompassLink").wait_for()

    expect(
        page.locator(".client-error"),
        "Elements with class 'client-error' found, failing the test.",
    ).not_to_be_visible()

    print("Test passed, no elements with class 'client-error' found.")
