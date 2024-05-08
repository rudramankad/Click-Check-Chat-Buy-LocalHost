from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "C:\\downloads\\chromedriver.exe"

implicit_wait_time = 3

url = 'https://southern-lane-419906.uc.r.appspot.com/'  

driver = webdriver.Chrome(executable_path="C:\\downloads\\chromedriver.exe")

driver.implicitly_wait(implicit_wait_time)


driver.get(url)

expected_title = "Click Check Chat Buy - Meet and chat with the sellers"
assert driver.title == expected_title, f"Expected title: {expected_title}, Actual title: {driver.title}"

search_bar = driver.find_element(By.ID, "searchInput")

expected_placeholder = "Search Items....."
assert search_bar.get_attribute("placeholder") == expected_placeholder, \
    f"Expected placeholder: {expected_placeholder}, Actual placeholder: {search_bar.get_attribute('placeholder')}"

search_term = "electronics"
search_bar.send_keys(search_term)

search_button = driver.find_element(By.CLASS_NAME, "btn-primary")
search_button.click()

search_results = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "searchResults"))
)

assert search_results.is_displayed(), "Search results are not displayed"

category_list = driver.find_element(By.CLASS_NAME, "list-group")
categories = category_list.find_elements(By.TAG_NAME, "a")

assert len(categories) > 0, "Categories are not listed"

driver.quit()