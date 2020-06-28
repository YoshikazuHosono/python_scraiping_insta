
# https://www.instagram.com/
# https://www.instagram.com/mai_tano/
# https://www.instagram.com/mai_tano/followers/

# "C:\00_BOX\chromedriver_win32\chromedriver.exe"

# https://qiita.com/memakura/items/20a02161fa7e18d8a693

import time
from selenium import webdriver
import requests
import json

def button_click(button_text):
    buttons = driver.find_elements_by_tag_name("button")

    for button in buttons:
        if button.text == button_text:
            button.click()
            break

driver = webdriver.Chrome('C:\\00_BOX\\selenium_driver\\chrome\\win\\83.0.4103.39\\chromedriver.exe')
driver.get('https://www.instagram.com/')

time.sleep(5)

driver.find_element_by_name("username").send_keys('yyhhwork@gmail.com')
driver.find_element_by_name("password").send_keys('tesla12coil')
button_click("ログイン")
time.sleep(5)

if driver.current_url == "https://www.instagram.com/accounts/onetap/?next=%2F":
    button_click("後で")
    time.sleep(5)

driver.get('https://www.instagram.com/mai_tano/')
time.sleep(5)

session = requests.session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie["name"], cookie["value"])

driver.quit()

result = session.get('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"1632264012","include_reel":false,"fetch_mutual":true,"first":30}')

data = json.loads(result.text)

list = data["data"]["user"]["edge_followed_by"]["edges"]
for node in list:
    print(node["node"]["username"])
