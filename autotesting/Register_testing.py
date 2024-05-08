from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chromedriver_path = "C:\\downloads\\chromedriver.exe"

implicit_wait_time = 3

url = 'https://southern-lane-419906.uc.r.appspot.com/accounts/register/'

driver = webdriver.Chrome(executable_path=chromedriver_path)

driver.implicitly_wait(implicit_wait_time)

driver.get(url)

expected_title = "User Registration Page"
assert driver.title == expected_title, f"Expected title: {expected_title}, Actual title: {driver.title}"

first_name_field = driver.find_element(By.ID, "first_name")

assert first_name_field.is_displayed(), "First Name field is not displayed"

last_name_field = driver.find_element(By.ID, "last_name")
assert last_name_field.is_displayed(), "Last Name field is not displayed"

email_field = driver.find_element(By.ID, "email")
assert email_field.is_displayed(), "Email field is not displayed"

username_field = driver.find_element(By.ID, "username")
assert username_field.is_displayed(), "Username field is not displayed"

password_field = driver.find_element(By.ID, "password")
assert password_field.is_displayed(), "Password field is not displayed"

register_button = driver.find_element(By.TAG_NAME, "button")

assert register_button.is_displayed(), "Register button is not displayed"

first_name_field.send_keys("")
last_name_field.send_keys("Last Name")
email_field.send_keys("user@example.com")
username_field.send_keys("test_user")
password_field.send_keys("Password123")
register_button.click()

error_message = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
)
assert error_message.is_displayed(), "Error message not displayed for empty first name"

driver.quit()
