from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def get_gender(driver, link):
    driver.get(link)

    # click 'About'
    try:
        element = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[2]/div[3]/ul/li[2]/a'))
        )
        element.click()
    except: # Cannot load
        return 'undefined'

    # click 'Basic Information'
    try:
        element = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[2]/div/ul/li/div/div[1]/div/div/div/a[4]'))
        )
        element.click()
    except: # Cannot load
        return 'undefined'
    

    # try to get gender
    try:
        box = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, 'collection_wrapper_2327158227'))
        )
        WebDriverWait(driver, 1).until(
            EC.text_to_be_present_in_element((By.ID, 'collection_wrapper_2327158227'), 'Gender')
        )
    except:
        return 'undefined'
    # time.sleep(0.5)
    arr = driver.find_elements_by_class_name('_2iem')
    for elem in arr:
        value = elem.get_attribute('innerHTML')
        if value == 'Female' or value == 'Male':
            return value
    
    return 'undefined'