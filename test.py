from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# https://chromedriver.chromium.org/downloads
PATH = "C:\Program Files (x86)\chromedriver.exe"

WINDOW_SIZE = "1920,1080"
chrome_options = Options()  
chrome_options.add_argument("--headless") # run background
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(executable_path=PATH,
					options=chrome_options
					)  
driver.get("http://thevuong8000.github.io")

try:
	WebDriverWait(driver, 5).until(
		EC.text_to_be_present_in_element((By.XPATH, '/html/body'), 'REPLY')
	)
	print("ok")
except:
	print("doesn't work")
driver.close()