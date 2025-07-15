from playwright.sync_api import sync_playwright
from pytest_bdd import given, when, then, scenarios
import pytest

# Use the scenarios function to link the feature file to this test file.
# We pass in the file path to our feature file.
scenarios("../login.feature")

# A Pytest fixture to manage the Playwright browser context.
# This ensures a new browser is opened for each test.
@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()

# The code for the "Given" step. This function will be called when the test
# sees the line "Given the user is on the login page" in the feature file.
@given("the user is on the login page")
def on_login_page(page):
    page.goto("https://www.saucedemo.com/")
    # We can add a check to make sure the page loaded correctly
    assert "Swag Labs" in page.title()

# The code for the "When" step. It defines the action of logging in.
@when("the user logs in with valid credentials")
def login_with_valid_credentials(page):
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

# The code for the "Then" step. It defines the expected outcome.
@then("the user should be redirected to the products page")
def redirected_to_products_page(page):
    # We will now check for the unique page title "Products"
    # This is a much more reliable way to confirm we are on the right page.
    assert page.get_by_text("Products").is_visible()
    assert "inventory.html" in page.url
