from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time, json

# https://chromedriver.chromium.org/downloads
PATH = "./tools/chromedriver.exe"

WINDOW_SIZE = "1920,1080"
chrome_options = Options()  
# chrome_options.add_argument("--headless") # run background
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

with open('./account/leetcode.json', 'r') as file:
	data = json.load(file)
	username = data['username']
	password = data['password']

driver = webdriver.Chrome(executable_path=PATH,
							options=chrome_options
							)  
driver.get("http://leetcode.com")

# error and stop the program
def error(message):
	print(message)
	driver.quit()
	exit()

# load the page
try:
	WebDriverWait(driver, 5).until(
		EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div/div/div[1]/div[3]/div[1]/div/div/div[2]/div/a[5]'))
	)
except TimeoutError:
	print("It took too long to get response from server!!!")
# time.sleep(1)

# click Sign in
driver.find_element_by_xpath('//*[@id="landing-page-app"]/div/div[1]/div[3]/div[1]/div/div/div[2]/div/a[5]/span').click()

# try to access login page
try:
	element = WebDriverWait(driver, 10).until(
		# check if 'Sign in' button could be clickable
		EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/button'))
	)

	# fill out username and password
	login_path = driver.find_element_by_id('id_login')
	login_path.send_keys(username)

	password_path = driver.find_element_by_id('id_password')
	password_path.send_keys(password)
	element.click()
except:
	error("It took too long to get response from server!!!")

# check if the bot can access to LeetCode homepage 
try:
	WebDriverWait(driver, 8).until(
		EC.title_contains('LeetCode - The World\'s Leading Online Programming Learning Platform')
	)
except TimeoutError:
	error("It took too long to get response from server!!!")
except:
	error("Your username or password is not correct!!! Please check again!")
print("Login successfully!!!")

driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/ul[1]/li[3]/a').click()
try:
	WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.CLASS_NAME, 'question-list-table'))
	)
except:
	error("It took too long to get response from server!!!")
print("Page loaded!!!")

