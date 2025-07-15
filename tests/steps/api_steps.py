from pytest_bdd import given, when, then, scenarios, parsers
import requests
import pytest

# Link this file to our API feature file
scenarios("../api.feature")

# This fixture will store the API response so it can be accessed by other steps
@pytest.fixture
def context():
    return {} # A simple dictionary to share data between steps

@given("the Fake Store API is available")
def api_available():
    base_url = "https://fakestoreapi.com/"
    try:
        response = requests.get(base_url, timeout=5)  # Add a timeout for robustness
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print(f"API is available! Status: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"API is not reachable: {e}")
    except requests.exceptions.Timeout:
        pytest.fail(f"API request timed out after 5 seconds: {base_url}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API request failed: {e}")
    pass

@when("a request is made to retrieve all products")
def get_all_products(context):
    # Make the GET request to the products endpoint
    response = requests.get("https://fakestoreapi.com/products")
    # Store the response in the context fixture for later steps
    context["response"] = response

@then("the response status code should be 200")
def check_status_code(context):
    assert context["response"].status_code == 200

@then("the response should contain a list of products")
def check_response_is_list(context):
    # Parse the JSON response
    products = context["response"].json()
    # Assert that it's a list (or at least an iterable) and not empty
    assert isinstance(products, list)
    assert len(products) > 0
    # Optional: Check structure of first item
    if products:
        assert "id" in products[0]
        assert "title" in products[0]
        assert "price" in products[0]

@when(parsers.parse("a request is made to retrieve product with ID \"{product_id}\""))
def get_single_product(context, product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.get(url)
    context["response"] = response
# NEW STEP DEFINITION for checking details for a specific product ID
@then(parsers.parse("the response should contain details for product ID \"{expected_id}\""))
def check_single_product_details(context, expected_id):
    product = context["response"].json()
    assert isinstance(product, dict) # Expecting a single product dictionary
    assert "id" in product
    assert str(product["id"]) == expected_id # Convert to string for comparison

# NEW STEP DEFINITION for checking the product title
@then(parsers.parse("the product title should be \"{expected_title}\""))
def check_product_title(context, expected_title):
    product = context["response"].json()
    assert "title" in product
    actual_title = product["title"]
    print(f"DEBUG: Expected Title: '{expected_title}'")
    print(f"DEBUG: Actual Title from API: '{actual_title}'")
    assert product["title"] == expected_title