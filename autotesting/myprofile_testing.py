from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "C:\\downloads\\chromedriver.exe"

implicit_wait_time = 3

url = 'https://southern-lane-419906.uc.r.appspot.com/myprofile/'

driver = webdriver.Chrome(executable_path=chromedriver_path)

driver.implicitly_wait(implicit_wait_time)

driver.get(url)

expected_title = "My Profile"  
assert driver.title == expected_title, f"Expected title: {expected_title}, Actual title: {driver.title}"

user_full_name_heading = driver.find_element(By.TAG_NAME, "h2")

assert user_full_name_heading.is_displayed(), "User Full Name heading is not displayed"

uploaded_items_container = driver.find_element(By.CLASS_NAME, "row")  

assert uploaded_items_container.is_displayed(), "Uploaded Items container is not displayed"


item_cards = driver.find_elements(By.CLASS_NAME, "card")

assert len(item_cards) > 0, "No item cards found in Uploaded Items"

driver.quit()
