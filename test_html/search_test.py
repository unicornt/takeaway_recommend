from login_test import *
from selenium.webdriver.common.keys import Keys

elem = browser.find_element_by_id('basic-url')
elem.send_keys('牛肉')
elem = browser.find_element_by_css_selector(".input-group > button")
elem.click()