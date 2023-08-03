import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@pytest.fixture(scope="module")
def driver():
    # Set up Chrome WebDriver with the specified executable path
    service = Service(executable_path='C:/Users/LENOVO/Gensis/chromedriver-win64/chromedriver.exe')  
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Optional: Run Chrome in headless mode
    #options.add_argument("--no-sandbox")  # Required for running in headless mode on some systems
    #options.add_argument("--disable-dev-shm-usage")  # Required for running in headless mode on some systems
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

    
# Global variable to store the previously clicked seat column
previous_column = -1


def test_ryanair_booking_flow(driver):
   # Step 1
    driver.get("https://www.ryanair.com/")
    assert "Ryanair" in driver.title, "Home Ryanair page is not loaded"

    # Step 2
    departure_city = "Dublin"
    destination_city = "Barcelona"
    desired_month_dept = "Nov"  
    desired_month_retu = "Dec"  
    departure_date = "2023-11-26"
    return_date = "2023-12-22"

    # Wait for the element to be clickable before clicking on it
    cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-ref='cookie.accept-all']")))
    cookie_button.click()

    subscriber_widget = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='subscriber-widget__mail-wrapper']")))
    subscriber_widget.click()

    # Search for flights
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-button__departure")))
    search_input.send_keys(Keys.BACKSPACE * len(search_input.get_attribute("value")))
    search_input.send_keys(departure_city)

    destination_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-button__destination")))
    destination_input.clear()
    destination_input.send_keys(destination_city)

    # Wait for the destination city to be selectable before clicking on it
    destination_city_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[@data-ref='airport-item__name' and contains(text(), '{destination_city}')]")))
    destination_city_element.click()

    # Find the element by XPath using the 'desired_month_dept' variable
    departure_month_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'm-toggle__month') and text()=' {desired_month_dept} ']")))
    departure_month_element.click()

    # Find the element by XPath using the 'departure_date' variable
    departure_date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='calendar-body__cell calendar-body__cell--weekend' and @tabindex='0' and @data-id='{departure_date}']")))
    departure_date_element.click()

    # Find the element by XPath using the 'desired_month_retu' variable
    return_month_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'm-toggle__month') and text()=' {desired_month_retu} ']")))
    return_month_element.click()

    # Find the element by XPath using the 'return_date' variable
    return_date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='calendar-body__cell' and @tabindex='0' and @data-id='{return_date}']")))
    return_date_element.click()

    # Find the element by XPath using the 'data-ref' attribute
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-ref='counter.counter__value']")))
    counter_value = int(element.text)
    num_adults = "2"

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

    assert "Dublin" in search_input.get_attribute("value"), "Departure city not set correctly"
    assert "Barcelona" in destination_input.get_attribute("value"), "Destination city not set correctly"
    assert desired_month_dept in driver.page_source, f"Desired departure month '{desired_month_dept}' not found in page source"
    assert desired_month_retu in driver.page_source, f"Desired return month '{desired_month_retu}' not found in page source"
    assert "2" in element.text, "Number of adults not set correctly"

    # Wait for the 'Continue' button to be clickable before clicking on it
    continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-ref='flight-search-widget__cta']")))
    continue_button.click()

   # Step 3
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
    assert "Passengers" in driver.page_source, "Passengers section not found"

    # Select title for passenger 1
    dropdown_toggle = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @aria-haspopup='true' and @class='dropdown__toggle body-l-lg body-l-sm' and @aria-expanded='false']")))
    dropdown_toggle.click()

    title1_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[@class='dropdown-item__link dropdown-item__link--highlighted']//div[@class='dropdown-item__content']//div[@class='dropdown-item__label body-l-lg body-l-sm' and text()=' {title1} ']")))
    title1_option.click()

    # Enter name and surname for passenger 1
    input_field = driver.find_element(By.ID, "form.passengers.ADT-0.name")
    input_field.send_keys(name1)
    input_field = driver.find_element(By.ID, "form.passengers.ADT-0.surname")
    input_field.send_keys(surname1)

    # Select title for passenger 2
    dropdown_toggle = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='dropdown__toggle body-l-lg body-l-sm' and @aria-haspopup='true']")))
    dropdown_toggle.click()

    title2_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[@class='dropdown-item__link dropdown-item__link--highlighted']//div[contains(@class, 'dropdown-item__label') and text()=' {title2} ']")))
    title2_option.click()

    # Enter name and surname for passenger 2
    input_field = driver.find_element(By.ID, "form.passengers.ADT-1.name")
    input_field.send_keys(name2)
    input_field = driver.find_element(By.ID, "form.passengers.ADT-1.surname")
    input_field.send_keys(surname2)

    # Assert passenger information
    assert WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, "form.passengers.ADT-0.name"), name1))
    assert WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, "form.passengers.ADT-0.surname"), surname1))
    assert WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, "form.passengers.ADT-1.name"), name2))
    assert WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, "form.passengers.ADT-1.surname"), surname2))

    # Click on the 'Continue' button
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

    # Click the 'Pick these seats' button
    try:
        pick_seats_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@ry-button and @color='anchor-blue' and contains(text(), 'Pick these seats')]")))
        pick_seats_button.click()
    except TimeoutException as e:
        print("The 'Pick these seats' button is not present on the page. Selecting return seats instead.")
        # Select the return seats using the same logic as before
        third_available_seat = find_next_available_seat(18, 0)
        if third_available_seat:
            driver.find_element(By.ID, third_available_seat).click()

        fourth_available_seat = find_next_available_seat(18, 0)  # Start searching from column 0 again
        if fourth_available_seat:
            driver.find_element(By.ID, fourth_available_seat).click()
    # Dismiss any pop-ups
    try:
        # Try to find and click the element to dismiss the pop-up
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-ref='enhanced-takeover-beta-desktop__dismiss-cta' and text()=' No, thanks ']"))).click()
    except TimeoutException:
        # If the element is not found, do nothing and continue with the rest of the code
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@_ngcontent-ng-c3388265545 and @ry-button and @class='passenger-carousel__button-next ry-button ry-button--gradient-yellow ry-button--flat-blue' and @data-ref='seats-action__button-continue']"))).click()

    # Add additional waits as needed for other elements and actions

    assert True, "The test completed successfully!"