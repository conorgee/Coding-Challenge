import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

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
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@data-ref='cookie.accept-all']").click()    
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='subscriber-widget__mail-wrapper']").click()
    time.sleep(1)

    # Search for flights
    search_input = driver.find_element(By.ID, "input-button__departure")
    search_input.send_keys(Keys.BACKSPACE * len(search_input.get_attribute("value")))
    search_input.send_keys(departure_city)
    time.sleep(1)
    destination_input = driver.find_element(By.ID, "input-button__destination")
    destination_input.clear()
    destination_input.send_keys(destination_city)
    time.sleep(1)
    driver.find_element(By.XPATH, f"//span[@data-ref='airport-item__name' and contains(text(), '{destination_city}')]").click()
    time.sleep(1)

    # Find the element by XPath using the 'desired_month_dept' variable
    driver.find_element(By.XPATH, f"//div[contains(@class, 'm-toggle__month') and text()=' {desired_month_dept} ']").click()   
    time.sleep(1)
    # Find the element by XPath using the 'departure_date' variable
    driver.find_element(By.XPATH, f"//div[@class='calendar-body__cell calendar-body__cell--weekend' and @tabindex='0' and @data-id='{departure_date}']").click()
    time.sleep(1)
    # Find the element by XPath using the 'desired_month_retu' variable
    driver.find_element(By.XPATH, f"//div[contains(@class, 'm-toggle__month') and text()=' {desired_month_retu} ']").click()
    time.sleep(1)
    # Find the element by XPath using the 'return_date' variable
    driver.find_element(By.XPATH, f"//div[@class='calendar-body__cell' and @tabindex='0' and @data-id='{return_date}']").click()
    time.sleep(1)
    # Find the element by XPath using the 'data-ref' attribute
    element = driver.find_element(By.XPATH, "//div[@data-ref='counter.counter__value']")
    counter_value = int(element.text)
    num_adults = "2"
    time.sleep(1)
    # Loop to increment or decrement the counter value until it matches the num_adults value
    while counter_value != int(num_adults):
        if counter_value < int(num_adults):
            # Increment the counter value
            driver.find_element(By.XPATH, "//div[@data-ref='counter.counter__increment']").click()
            counter_value+=1
            time.sleep(1)
        else:
            # Decrement the counter value
            driver.find_element(By.XPATH, "//div[@data-ref='counter.counter__decrement']").click()
            counter_value-=1
            time.sleep(1)

    assert "Dublin" in search_input.get_attribute("value"), "Departure city not set correctly"
    assert "Barcelona" in destination_input.get_attribute("value"), "Destination city not set correctly"
    assert desired_month_dept in driver.page_source, f"Desired departure month '{desired_month_dept}' not found in page source"
    assert desired_month_retu in driver.page_source, f"Desired return month '{desired_month_retu}' not found in page source"
    assert "2" in element.text, "Number of adults not set correctly"

    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@data-ref='flight-search-widget__cta']").click()
    time.sleep(4)

    # Step 3
    current_url = driver.current_url
    assert departure_date in current_url, f"Departure date '{departure_date}' not present in the URL after selection"
    assert return_date in current_url, f"Return date '{return_date}' not present in the URL after selection"

    driver.find_element(By.XPATH, "//button[@_ngcontent-ng-c2051464752 and @ry-button='' and @color='gradient-blue']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@_ngcontent-ng-c2051464752=''and @ry-button='' and @color='gradient-blue']").click()
    time.sleep(10)

    # Choosing regular 
    # Check if the first element is present
    if driver.find_elements(By.XPATH, '//div[@class="fare-table__fare-column-border" and @data-e2e="fare-card--regu"]'):
        # If the first element is present, click on it
        driver.find_element(By.XPATH, '//div[@class="fare-table__fare-column-border" and @data-e2e="fare-card--regu"]').click()
    else:
        # If the first element is not present, click on the second element
        driver.find_element(By.XPATH, "//button[@_ngcontent-ng-c3204906501 and @ry-button and @class='fare-card__button fare-card__price ry-button--gradient-light-blue']").click()
    time.sleep(10)
    
    assert "Log in later" in driver.page_source, "Log in to myRyanair section not found"

    # Step 4
    driver.find_element(By.XPATH, "//button[@color='anchor-blue' and @class='login-touchpoint__expansion-bar']").click()
    time.sleep(1)
    
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
    driver.find_element(By.XPATH, "//button[@type='button' and @aria-haspopup='true' and @class='dropdown__toggle body-l-lg body-l-sm' and @aria-expanded='false']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, f"//button[@class='dropdown-item__link dropdown-item__link--highlighted']//div[@class='dropdown-item__content']//div[@class='dropdown-item__label body-l-lg body-l-sm' and text()=' {title1} ']").click()
    time.sleep(1)

    # Enter name and surname for passenger 1
    input_field = driver.find_element(By.ID, "form.passengers.ADT-0.name")
    input_field.send_keys(name1)
    input_field = driver.find_element(By.ID, "form.passengers.ADT-0.surname")
    input_field.send_keys(surname1)

    # Select title for passenger 2
    driver.find_element(By.XPATH, "//button[@class='dropdown__toggle body-l-lg body-l-sm' and @aria-haspopup='true']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, f"//button[@class='dropdown-item__link dropdown-item__link--highlighted']//div[contains(@class, 'dropdown-item__label') and text()=' {title2} ']").click()
    time.sleep(1)

    # Enter name and surname for passenger 2
    input_field = driver.find_element(By.ID, "form.passengers.ADT-1.name")
    input_field.send_keys(name2)
    input_field = driver.find_element(By.ID, "form.passengers.ADT-1.surname")
    input_field.send_keys(surname2)

    assert driver.find_element(By.ID, "form.passengers.ADT-0.name").get_attribute("value") == name1
    assert driver.find_element(By.ID, "form.passengers.ADT-0.surname").get_attribute("value") == surname1
    assert driver.find_element(By.ID, "form.passengers.ADT-1.name").get_attribute("value") == name2
    assert driver.find_element(By.ID, "form.passengers.ADT-1.surname").get_attribute("value") == surname2

    # Click on the 'Continue' button
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@ry-button and @color='gradient-yellow' and contains(text(), 'Continue')]").click()


    # # Step 6/7
    # time.sleep(4)
    # driver.find_element(By.ID, "seat-18A").click()
    # driver.find_element(By.ID, "seat-18B").click()
    # time.sleep(2)
    # driver.find_element(By.XPATH, "//button[@class='passenger-carousel__button-next ry-button ry-button--gradient-yellow ry-button--flat-blue' and @data-ref='seats-action__button-next']").click()
    # time.sleep(4)
    # driver.find_element(By.XPATH, "//button[@ry-button and @color='anchor-blue' and contains(text(), 'Pick these seats')]").click()
    # time.sleep(5)
    # driver.find_element(By.XPATH, "//button[@data-ref='enhanced-takeover-beta-desktop__dismiss-cta' and text()=' No, thanks ']").click()
    # time.sleep(3)

    time.sleep(4)

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


    # Click the 'Next' button
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@class='passenger-carousel__button-next ry-button ry-button--gradient-yellow ry-button--flat-blue' and @data-ref='seats-action__button-next']").click()
    time.sleep(4)

    #  Click the 'Pick these seats' button
    # driver.find_element(By.XPATH, "//button[@ry-button and @color='anchor-blue' and contains(text(), 'Pick these seats')]").click()
    # time.sleep(5)
    time.sleep(3)

    try:
        pick_seats_button = driver.find_element(By.XPATH, "//button[@ry-button and @color='anchor-blue' and contains(text(), 'Pick these seats')]")
        pick_seats_button.click()
        time.sleep(5)
    except NoSuchElementException:
        # Handle the case when the button is not found
        print("The 'Pick these seats' button is not present on the page. Selecting return seats instead.")
    # Select the return seats using the same logic as before
    
        third_available_seat = find_next_available_seat(18, 0)
        if third_available_seat:
            driver.find_element(By.ID, third_available_seat).click()

        fourth_available_seat = find_next_available_seat(18, 0)  # Start searching from column 0 again
        if fourth_available_seat:
            driver.find_element(By.ID, fourth_available_seat).click()

    time.sleep(5)    

    # Dismiss any pop-ups
    try:
        # Try to find and click the element to dismiss the pop-up
        driver.find_element(By.XPATH, "//button[@data-ref='enhanced-takeover-beta-desktop__dismiss-cta' and text()=' No, thanks ']").click()
    except NoSuchElementException:
        # If the element is not found, do nothing and continue with the rest of the code
        driver.find_element(By.XPATH, "//button[@_ngcontent-ng-c3388265545 and @ry-button and @class='passenger-carousel__button-next ry-button ry-button--gradient-yellow ry-button--flat-blue' and @data-ref='seats-action__button-continue']").click()  
        pass

    #
    # Presses continue on seats page
    # 
    # driver.find_element(By.XPATH, "//button[@_ngcontent-ng-c3388265545 and @ry-button and @class='passenger-carousel__button-next ry-button ry-button--gradient-yellow ry-button--flat-blue' and @data-ref='seats-action__button-continue']").click()  
    time.sleep(4)

    assert True, "The test completed successfully!"
 