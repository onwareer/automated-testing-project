 Feature: User login functionality

  Scenario: Successful login with valid credentials
    Given the user is on the login page
    When the user logs in with valid credentials
    Then the user should be redirected to the products page

  Scenario: Add an item to the cart and verify
    Given the user is logged in
    When the user adds a "Sauce Labs Backpack" to the cart
    Then the cart should contain "1" item

  Scenario: Complete a checkout flow
    Given the user has a "Sauce Labs Backpack" in the cart
    When the user completes the checkout process
    Then the order confirmation message is displayed
