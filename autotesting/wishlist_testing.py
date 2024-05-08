from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "C:\\downloads\\chromedriver.exe"

implicit_wait_time = 3

url = 'https://southern-lane-419906.uc.r.appspot.com/wishlist/'

driver = webdriver.Chrome(executable_path=chromedriver_path)

driver.implicitly_wait(implicit_wait_time)

driver.get(url)

expected_title = "Shopping wish list"  
assert driver.title == expected_title, f"Expected title: {expected_title}, Actual title: {driver.title}"

wishlist_table_container = driver.find_element(By.CLASS_NAME, "table")

assert wishlist_table_container.is_displayed(), "Shopping Wish List table is not displayed"

table_headers = driver.find_elements(By.TAG_NAME, "th")

assert len(table_headers) >= 5, "Expected at least 5 table headers, found only {}".format(len(table_headers))
expected_headers = ["Product", "Price", "Quantity", "Total", "Actions"]
for header in expected_headers:
    assert header in [th.text for th in table_headers], f"Header '{header}' not found in table"

remove_button = driver.find_element(By.CLASS_NAME, "remove-btn")

assert remove_button.is_displayed(), "Remove button not found in wishlist"

view_product_button = driver.find_element(By.CLASS_NAME, "btn-primary")

assert view_product_button.is_displayed(), "View product button not found in wishlist"

driver.quit()