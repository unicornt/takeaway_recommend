from selenium import webdriver
from selenium.webdriver import ActionChains
import time
browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('http://127.0.0.1:8000')
browser.maximize_window()
time.sleep(2)
elem = browser.find_element_by_id("login-button")
ActionChains(browser).move_to_element(elem).click(elem).perform()
username_input = browser.find_element_by_name("usr")
username_input.send_keys('jason')
password_input = browser.find_element_by_name("pwd")
password_input.send_keys('1234')
browser.implicitly_wait(10)
login_button = browser.find_element_by_id("login")
ActionChains(browser).move_to_element(login_button).click(login_button).perform()