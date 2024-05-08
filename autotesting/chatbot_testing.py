from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "C:\\downloads\\chromedriver.exe"

implicit_wait_time = 3

url = 'https://southern-lane-419906.uc.r.appspot.com/chat/965127635476807681/'

driver = webdriver.Chrome(executable_path=chromedriver_path)

driver.implicitly_wait(implicit_wait_time)

driver.get(url)

expected_title = "Chat screen"
assert driver.title == expected_title, f"Expected title: {expected_title}, Actual title: {driver.title}"

go_back_button = driver.find_element(By.TAG_NAME, "button")

assert go_back_button.is_displayed(), "Go Back to Homepage button is not displayed"

chat_container = driver.find_element(By.ID, "message-container")

assert chat_container.is_displayed(), "Chat conversation container is not displayed"

username_element = driver.find_element(By.CLASS_NAME, "heading-name-meta")

assert username_element.is_displayed(), "Username is not displayed in chat heading"

message_input = driver.find_element(By.ID, "comment")

assert message_input.is_displayed(), "Chat message input field is not displayed"

send_button = driver.find_element(By.CLASS_NAME, "reply-send").find_element(By.TAG_NAME, "button")

assert send_button.is_displayed(), "Send message button is not displayed"

driver.quit()