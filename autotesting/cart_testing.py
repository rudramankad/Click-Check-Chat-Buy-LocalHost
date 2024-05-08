from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "C:\\downloads\\chromedriver.exe"
implicit_wait_time = 3

url = 'https://southern-lane-419906.uc.r.appspot.com/cart'

driver = webdriver.Chrome(executable_path=chromedriver_path)

driver.implicitly_wait(implicit_wait_time)

driver.get(url)

expected_title = "Cart - Click Check Chat Buy"
assert driver.title == expected_title, f"Expected title: {expected_title}, Actual title: {driver.title}"

cart_heading = driver.find_element(By.TAG_NAME, "h1")

assert cart_heading.is_displayed(), "Shopping Cart heading is not displayed"

cart_table = driver.find_element(By.TAG_NAME, "table")

assert cart_table.is_displayed(), "Cart table is not displayed"

table_headers = cart_table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")
expected_headers = ["Product", "Price", "Quantity", "Total", "Actions"]
assert len(table_headers) == len(expected_headers), "Incorrect number of table headers"

for i in range(len(expected_headers)):
    assert expected_headers[i] == table_headers[i].text, f"Incorrect table header: {i+1}"

continue_shopping_button = driver.find_element(By.LINK_TEXT, "Continue Shopping")

assert continue_shopping_button.is_displayed(), "Continue Shopping button is not displayed"

total_amount_element = driver.find_element(By.ID, "total-amount")

assert total_amount_element.is_displayed(), "Total amount element is not displayed"

driver.quit()