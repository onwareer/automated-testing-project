 Feature: Product API functionality

  Scenario: Retrieve all products
    Given the Fake Store API is available
    When a request is made to retrieve all products
    Then the response status code should be 200
    And the response should contain a list of products

Scenario: Retrieve a single product by ID
    Given the Fake Store API is available
    When a request is made to retrieve product with ID "1"
    Then the response status code should be 200
    And the response should contain details for product ID "1"
    And the product title should be "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops"
    And the product response should conform to schema