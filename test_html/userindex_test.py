from login_test import *

elem = browser.find_element_by_id("navbarDropdown")
ActionChains(browser).move_to_element(elem).click(elem).perform()
time.sleep(2)
elem = browser.find_element_by_link_text("个人主页")
ActionChains(browser).move_to_element(elem).click(elem).perform()
elem = browser.find_element_by_id("dropdownMenuButton")
ActionChains(browser).move_to_element(elem).click(elem).perform()
elem = browser.find_element_by_link_text("被赞数")
elem.click()
time.sleep(2)
elem = browser.find_element_by_link_text("上传时间")
elem.click()