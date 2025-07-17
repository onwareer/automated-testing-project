from faker import Faker
from playwright.sync_api import sync_playwright
from pytest_bdd import given, when, then, scenarios, parsers
import pytest


from tests.utils.visual import assert_visual_match

scenarios("../login.feature")
fake = Faker()


@pytest.fixture
def page():
    with sync_playwright() as p:
        # We'll run in headless mode for CI/CD, but you can change to
        # headless=False to see the browser during development
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()

@given("the user is on the login page")
def on_login_page(page):
    page.goto("https://www.saucedemo.com/")
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


@then("the products page layout should be visually correct")
def visual_check_products_page(page):
    page.wait_for_selector("text=Products")
    assert_visual_match(page, "products_page")

# The code for the "Given the user is logged in" step.
# This makes our test more modular, so we don't have to repeat the login code.
@given("the user is logged in")
def logged_in_user(page):
    page.goto("https://www.saucedemo.com/")
    assert "Swag Labs" in page.title()
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    assert page.get_by_text("Products").is_visible()

@given("the user has a \"Sauce Labs Backpack\" in the cart")
def add_backpack_to_cart(page):
    logged_in_user(page)
    page.click("button#add-to-cart-sauce-labs-backpack")
    assert page.locator(".shopping_cart_badge").is_visible()

@when(parsers.parse("the user adds a \"{item}\" to the cart"))
def add_item_to_cart(page, item):
    # This step uses a parser to extract the item name from the feature file
    # and use it to locate the correct "Add to cart" button.
    item_locator = f"button[id^='add-to-cart-'][name*='{item.replace(' ', '-').lower()}']"
    page.click(item_locator)

@when("the user completes the checkout process")
def complete_checkout_process(page):
    page.click(".shopping_cart_link")
    page.click("button#checkout")
    # Use Faker to generate dynamic data for the checkout form
    first_name = fake.first_name()
    last_name = fake.last_name()
    postal_code = fake.postcode()  # Generates a realistic postal code

    page.fill("input#first-name", "Test")
    page.fill("input#last-name", "User")
    page.fill("input#postal-code", "12345")
    page.click("input#continue")
    page.click("button#finish")

@then(parsers.parse("the cart should contain \"{count}\" item"))
def cart_contains_item(page, count):
    # This step uses a parser to verify the count of items in the cart.
    cart_count = page.locator(".shopping_cart_badge").inner_text()
    assert cart_count == count

@then("the order confirmation message is displayed")
def order_confirmation_displayed(page):
    # We check for the unique text on the confirmation page.
    assert page.get_by_text("Checkout: Complete!").is_visible()
    assert page.get_by_text("Thank you for your order!").is_visible()
    assert page.get_by_text("Your order has been dispatched").is_visible()




