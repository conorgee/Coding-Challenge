# Import necessary libraries and modules
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define a fixture named "driver" with scope set to "module"
@pytest.fixture(scope="module")
def driver():
    # Set up Chrome WebDriver with the specified executable path
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Optional: Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Required for running in headless mode on some systems
    options.add_argument("--disable-dev-shm-usage")  # Required for running in headless mode on some systems

    # Create an instance of the Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=options)

    # Yield the driver instance to the test function using this fixture
    yield driver

    # After the test function is executed, quit the driver to clean up resources
    driver.quit()
# Global variable to store the previously clicked seat column
previous_column = -1

def test_ryanair_booking_flow(driver):
    # Step 1: Open Ryanair website
    driver.get("https://www.ryanair.com/")
    assert "Ryanair" in driver.title, "Home Ryanair page is not loaded"

    # Step 2: Define search parameters for the flights
    departure_city = "Dublin"
    destination_city = "Barcelona"
    desired_month_dept = "Nov"
    desired_month_retu = "Dec"
    departure_date = "2023-11-26"
    return_date = "2023-12-22"

    # Wait for the cookie button to be clickable before clicking it
    cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-ref='cookie.accept-all']")))
    cookie_button.click()

    # Click on the subscriber widget to dismiss it
    subscriber_widget = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='subscriber-widget__mail-wrapper']")))
    subscriber_widget.click()

    # Search for flights by entering the departure city
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-button__departure")))
    search_input.send_keys(Keys.BACKSPACE * len(search_input.get_attribute("value")))
    search_input.send_keys(departure_city)

    # Clear the destination input field and enter the destination city
    destination_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-button__destination")))
    destination_input.clear()
    destination_input.send_keys(destination_city)

    # Wait for the destination city to be selectable before clicking on it
    destination_city_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[@data-ref='airport-item__name' and contains(text(), '{destination_city}')]")))
    destination_city_element.click()

    # Find and click the departure month using the 'desired_month_dept' variable
    departure_month_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'm-toggle__month') and text()=' {desired_month_dept} ']")))
    departure_month_element.click()

    # Find and click the departure date using the 'departure_date' variable
    departure_date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='calendar-body__cell calendar-body__cell--weekend' and @tabindex='0' and @data-id='{departure_date}']")))
    departure_date_element.click()

    # Find and click the return month using the 'desired_month_retu' variable
    return_month_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'm-toggle__month') and text()=' {desired_month_retu} ']")))
    return_month_element.click()

    # Find and click the return date using the 'return_date' variable
    return_date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='calendar-body__cell' and @tabindex='0' and @data-id='{return_date}']")))
    return_date_element.click()

    # Find and read the number of available seats for the selected flights
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-ref='counter.counter__value']")))
    counter_value = int(element.text)
    num_adults = "2"  # Number of adults for the booking, currently fixed at 2
# Loop to increment or decrement the counter value until it matches the num_adults value
while counter_value != int(num_adults):
    if counter_value < int(num_adults):
        # Increment the counter value
        increment_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-ref='counter.counter__increment']")))
        increment_button.click()
        counter_value += 1
    else:
        # Decrement the counter value
        decrement_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-ref='counter.counter__decrement']")))
        decrement_button.click()
        counter_value -= 1

    # Assert statements to check if certain conditions are met, or else raise an AssertionError
    assert "Dublin" in search_input.get_attribute("value"), "Departure city not set correctly"
    assert "Barcelona" in destination_input.get_attribute("value"), "Destination city not set correctly"
    assert desired_month_dept in driver.page_source, f"Desired departure month '{desired_month_dept}' not found in page source"
    assert desired_month_retu in driver.page_source, f"Desired return month '{desired_month_retu}' not found in page source"
    assert "2" in element.text, "Number of adults not set correctly"

    # Wait for the 'Continue' button to be clickable before clicking on it
    continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-ref='flight-search-widget__cta']")))
    continue_button.click()

    # Step 3
    # Get the current URL and perform assertions to check if specific dates are present in the URL
    current_url = driver.current_url
    assert departure_date in current_url, f"Departure date '{departure_date}' not present in the URL after selection"
    assert return_date in current_url, f"Return date '{return_date}' not present in the URL after selection"

    # Wait for the first button to be clickable and then click it
    wait = WebDriverWait(driver, 10)
    first_button_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@_ngcontent-ng-c2051464752]")))
    first_button_element.click()

    # Wait for the second button to be clickable and then click it
    second_button_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@_ngcontent-ng-c2051464752='' and @color='gradient-blue']")))
    second_button_element.click()

    # Choosing regular
    # Check if the first element is present
    try:
        # Explicit wait for the first element to be present
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="fare-table__fare-column-border" and @data-e2e="fare-card--regu"]')))
        # If the first element is present, click on it
        driver.find_element(By.XPATH, '//div[@class="fare-table__fare-column-border" and @data-e2e="fare-card--regu"]').click()
    except:
        # If the first element is not present, click on the second element
        driver.find_element(By.XPATH, "//button[@_ngcontent-ng-c3204906501 and @ry-button and @class='fare-card__button fare-card__price ry-button--gradient-light-blue']").click()

    # Explicit wait for "Log in later" text to be present in the page source
    wait.until(EC.text_to_be_present_in_element((By.XPATH, "//body"), "Log in later"))

    # Assert that "Log in later" is present in the driver's page source, otherwise raise an assertion error
    assert "Log in later" in driver.page_source, "Log in to myRyanair section not found"

    # Step 4
    # Explicit wait for the button to be clickable
    button_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@color='anchor-blue' and @class='login-touchpoint__expansion-bar']")))
    button_element.click()

    # Define variables for names and titles
    title1 = "Mr"
    name1 = "Joe"
    surname1 = "Bloggs"
    title2 = "Mr"
    name2 = "Jim"
    surname2 = "Bloggs"

    # Step 5
    # Assert that the "Passengers" section is present in the page source; otherwise, raise an error with the message "Passengers section not found"
    assert "Passengers" in driver.page_source, "Passengers section not found"

    # Select title for passenger 1
    # Find and click the dropdown toggle button for passenger 1 title selection
    dropdown_toggle = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @aria-haspopup='true' and @class='dropdown__toggle body-l-lg body-l-sm' and @aria-expanded='false']")))
    dropdown_toggle.click()

    # Find and click the option corresponding to the selected title for passenger 1
    title1_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[@class='dropdown-item__link dropdown-item__link--highlighted']//div[@class='dropdown-item__content']//div[@class='dropdown-item__label body-l-lg body-l-sm' and text()=' {title1} ']")))
    title1_option.click()

    # Enter name and surname for passenger 1
    # Find the input field for passenger 1 name and fill it with the provided name1 value
    input_field = driver.find_element(By.ID, "form.passengers.ADT-0.name")
    input_field.send_keys(name1)
    # Find the input field for passenger 1 surname and fill it with the provided surname1 value
    input_field = driver.find_element(By.ID, "form.passengers.ADT-0.surname")
    input_field.send_keys(surname1)

    # Select title for passenger 2
    # Find and click the dropdown toggle button for passenger 2 title selection
    dropdown_toggle = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='dropdown__toggle body-l-lg body-l-sm' and @aria-haspopup='true']")))
    dropdown_toggle.click()

    # Find and click the option corresponding to the selected title for passenger 2
    title2_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[@class='dropdown-item__link dropdown-item__link--highlighted']//div[contains(@class, 'dropdown-item__label') and text()=' {title2} ']")))
    title2_option.click()

    # Enter name and surname for passenger 2
    # Find the input field for passenger 2 name and fill it with the provided name2 value
    input_field = driver.find_element(By.ID, "form.passengers.ADT-1.name")
    input_field.send_keys(name2)
    # Find the input field for passenger 2 surname and fill it with the provided surname2 value
    input_field = driver.find_element(By.ID, "form.passengers.ADT-1.surname")
    input_field.send_keys(surname2)

    # Assert passenger information
    # Assert that the input field values for passenger 1 and passenger 2 match the provided name1, surname1, name2, and surname2 values respectively, within the given timeout (10 seconds).
    assert WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, "form.passengers.ADT-0.name"), name1))
    assert WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, "form.passengers.ADT-0.surname"), surname1))
    assert WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, "form.passengers.ADT-1.name"), name2))
    assert WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, "form.passengers.ADT-1.surname"), surname2))

    # Click on the 'Continue' button
    # Find and click the 'Continue' button with the specified attributes (button with the text 'Continue' and color 'gradient-yellow').
    continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@ry-button and @color='gradient-yellow' and contains(text(), 'Continue')]")))
    continue_button.click()
    
    # Custom function to check if a seat is available
    def is_seat_available(seat_id):
        try:
            seat = driver.find_element(By.ID, seat_id)
            return seat.get_attribute("class").find("seatmap__seat--unavailable") == -1
        except NoSuchElementException:
            return False

    # Function to find the next available seat
    def find_next_available_seat(seat_row, seat_column):
        global previous_column
        for row in range(seat_row, 34):  # Range from 18 to 33
            for column in range(seat_column, 7):  # Range from A to F
                if column == previous_column:
                    continue  # Skip the previously clicked column
                seat_id = f"seat-{row}{chr(ord('A') + column)}"
                if is_seat_available(seat_id):
                    previous_column = column  # Update the previously clicked column
                    return seat_id
        return None

    # Select the first available seat
    first_available_seat = find_next_available_seat(18, 0)
    if first_available_seat:
        driver.find_element(By.ID, first_available_seat).click()

    # Select the second available seat
    second_available_seat = find_next_available_seat(18, 0)  # Start searching from column 0 again
    if second_available_seat:
        driver.find_element(By.ID, second_available_seat).click()

    # Wait for the button to be clickable before clicking on it
    next_flight_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@_ngcontent-ng-c3388265545 and @ry-button and @class='passenger-carousel__button-next ry-button ry-button--gradient-yellow ry-button--flat-blue' and @data-ref='seats-action__button-next']")))
    next_flight_button.click()

    # Click the 'Pick these seats' button for return flights
    try:
        return_seats_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@ry-button and @color='anchor-blue' and contains(text(), 'Pick these seats')]")))
        return_seats_button.click()
    except TimeoutException as e:
        print("The 'Pick these seats' button is not present on the page. Selecting return seats instead.")
        # Select the return seats using the same logic as before
        return_flight_first_seat = find_next_available_seat(18, 0)
        if return_flight_first_seat:
            driver.find_element(By.ID, return_flight_first_seat).click()

        return_flight_second_seat = find_next_available_seat(18, 0)  # Start searching from column 0 again
        if return_flight_second_seat:
            driver.find_element(By.ID, return_flight_second_seat).click()

    # Dismiss any pop-ups
    try:
        # Try to find and click the element to dismiss the pop-up
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-ref='enhanced-takeover-beta-desktop__dismiss-cta' and text()=' No, thanks ']"))).click()
    except TimeoutException:
        # If the element is not found, do nothing and continue with the rest of the code
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@_ngcontent-ng-c3388265545 and @ry-button and @class='passenger-carousel__button-next ry-button ry-button--gradient-yellow ry-button--flat-blue' and @data-ref='seats-action__button-continue']"))).click()

    # Add additional waits as needed for other elements and actions

    assert True, "The test completed successfully!"
