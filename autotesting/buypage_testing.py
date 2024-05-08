from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "C:\\downloads\\chromedriver.exe"

implicit_wait_time = 3

url = 'https://southern-lane-419906.uc.r.appspot.com/buypage/965134102736797697/'

driver = webdriver.Chrome(executable_path=chromedriver_path)

driver.implicitly_wait(implicit_wait_time)

driver.get(url)

expected_title = "Click Check Chat Buy - Item Details" 
assert driver.title == expected_title, f"Expected title: {expected_title}, Actual title: {driver.title}"

item_name = driver.find_element(By.CLASS_NAME, "card-title")

assert item_name.is_displayed(), "Item name is not displayed"

item_image = driver.find_element(By.CLASS_NAME, "card-img-top")
assert item_image.is_displayed(), "Item image is not displayed"

chat_button = None
try:
    chat_button = driver.find_element(By.LINK_TEXT, "Chat with seller")
except:
    pass

if chat_button:
    assert chat_button.is_displayed(), "Chat button is not displayed for non-seller user"

item_description = driver.find_element(By.CLASS_NAME, "card-text").find_element(By.TAG_NAME, "p")

assert item_description.is_displayed(), "Item description is not displayed"

item_category = driver.find_element(By.XPATH, "//p[text()='Item Category:']")
item_condition = driver.find_element(By.XPATH, "//p[text()='Item Condition:']")
item_price = driver.find_element(By.XPATH, "//p[text()='Price:']")

assert item_category.is_displayed(), "Item category is not displayed"
assert item_condition.is_displayed(), "Item condition is not displayed"
assert item_price.is_displayed(), "Item price is not displayed"

wishlist_button = None
buy_button = None
try:
    wishlist_button = driver.find_element(By.CLASS_NAME, "btn-primary").find_element(By.LINK_TEXT, "Add to wishlist")
    buy_button = driver.find_element(By.CLASS_NAME, "btn-primary").find_element(By.LINK_TEXT, "Buy now")
except:
    pass

if not wishlist_button or not buy_button:
    print("Wishlist or Buy Now button not found. Login functionality not tested in this script.")

driver.quit()