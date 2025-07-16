from faker import Faker
from playwright.sync_api import sync_playwright
from pytest_bdd import given, when, then, scenarios, parsers
import pytest
from PIL import Image, ImageChops
import os
import shutil


scenarios("../login.feature")
fake = Faker()

def compare_images(baseline_path, current_path):
    baseline = Image.open(baseline_path)
    current = Image.open(current_path)
    diff = ImageChops.difference(baseline, current)
    return diff.getbbox() is None

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

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

    snapshots_dir = os.path.join(project_root, "snapshots")
    os.makedirs(snapshots_dir, exist_ok=True)

    baseline_path = os.path.join(snapshots_dir, "products_page_baseline.png")
    current_path = os.path.join(snapshots_dir, "products_page_current.png")

    #baseline_path = "snapshots/products_page_baseline.png"
    #current_path = "snapshots/products_page_current.png"

    print(f"[DEBUG] Saving screenshot to: {current_path}")
    os.makedirs("snapshots", exist_ok=True)
    page.wait_for_timeout(2000)  # Good for ensuring page is stable
    page.screenshot(path=current_path, full_page=True)
    # First time: save as baseline
    if not os.path.exists(baseline_path):
        print("[INFO] No baseline found. Saving current screenshot as baseline.")
        shutil.copy(current_path, baseline_path) # keep both baseline and current
        #os.rename(current_path, baseline_path)
        return
    assert compare_images(baseline_path, current_path), "Visual regression detected!"

    # IMPORTANT: Ensure the 'page.evaluate' line for simulating visual changes is
    # placed *before* page.screenshot(path=current_path, full_page=True)
    # ONLY when you want to demonstrate a failure.
    # Currently, assume it's NOT there for initial baseline creation.

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




