from selenium import webdriver
from selenium.webdriver import ActionChains
browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('http://127.0.0.1:8000')
elem = browser.find_element_by_id("login-button")
url=elem.get_attribute('href')
browser.get(url)
username_input = browser.find_element_by_name("usr")
username_input.send_keys('unicornt')
password_input = browser.find_element_by_name("pwd")
password_input.send_keys('123456')
browser.implicitly_wait(10)
login_button = browser.find_element_by_id("login")
ActionChains(browser).move_to_element(login_button).click(login_button).perform()