from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import accountinfo
import json, time

# https://chromedriver.chromium.org/downloads
PATH = "C:\Program Files (x86)\chromedriver.exe"

WINDOW_SIZE = "1920,1080"
chrome_options = Options()  
chrome_options.add_argument("--headless") # run background
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--disable-notifications")

with open('./account/facebook.json') as file:
	account = json.load(file)

# error and stop the program
def error(driver, message):
	print(message)
	driver.quit()
	exit()

class facebook_bot():
	def __init__(self):
		print("I'm in")
		self.male = 0
		self.female = 0
		self.driver = webdriver.Chrome(executable_path=PATH,
							options=chrome_options
							)  
		self.driver.get("http://facebook.com")

		# try to login
		try:
			element = WebDriverWait(self.driver, 10).until(
				# check if 'Sign in' button could be clickable
				EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/table/tbody/tr[2]/td[3]/label/input'))
			)

			# fill out username and password
			login_path = self.driver.find_element_by_id('email')
			login_path.send_keys(account['username'])

			password_path = self.driver.find_element_by_id('pass')
			password_path.send_keys(account['password'])
			element.click() # login
		except:
			error(self.driver, "It took too long to get response from server!!!")
		print("Login successfully!!!")

	def count_friends(self):
		# try to access profile page
		try:
			profile_page = WebDriverWait(self.driver, 5).until(
				EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/a'))
			)
			profile_page.click()
		except: 
			error(self.driver, "It took too long to get response from server!!!")
		
		# scroll down to load friends button
		while True:
			# Scroll down
			try:
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			except:
				pass
			friend_button = self.driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div/span/div/div/div[5]/div[1]/li/div/div/div/div[1]/div[2]/div/span[2]/a')
			if len(friend_button) != 0:
				break

		# try to access friends list
		# try:
		self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div/span/div/div/div[5]/div[1]/li/div/div/div/div[1]/div[2]/div/span[2]/a').click()
		
		# scroll to load all friends
		while True:
			# Scroll down
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			# break if load all friends
			end_line = self.driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/h3')
			if len(end_line) != 0:
				break
		time.sleep(2)
		friends = self.driver.find_elements_by_class_name('fcb')
		friends = friends[1:]
		friend_info = []
		for friend in friends:
			try:
				href = friend.find_element_by_tag_name('a')
				name = href.get_attribute('innerHTML')
				link = href.get_attribute('href')
				friend_info.append((name, link))
			except:
				pass
		print(len(friends), 'friends')
		actual_friends = 0
		for (name, link) in friend_info:
			if link[-1] == '#': # deactive account
				continue
			gender = accountinfo.get_gender(self.driver, link)
			# print(name, ":", link)
			print(name, ":", gender)
			if gender == 'Male':
				self.male += 1
			elif gender == 'Female':
				self.female += 1
			actual_friends += 1
		print(actual_friends, 'friends are active')
		print(f"There are {self.male} males and {self.female} females in your friend list!!!")


my_bot = facebook_bot()
my_bot.count_friends()
			