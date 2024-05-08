from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "C:\\downloads\\chromedriver.exe"

implicit_wait_time = 3

url = 'https://southern-lane-419906.uc.r.appspot.com/aboutus/'

driver = webdriver.Chrome(executable_path="C:\\downloads\\chromedriver.exe")

driver.implicitly_wait(implicit_wait_time)

driver.get(url)

about_section = driver.find_element(By.CLASS_NAME, 'about-section')

driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", about_section)

driver.execute_script("window.scrollTo(0, document.body.scrollTop);")

driver.quit()