
# https://www.instagram.com/
# https://www.instagram.com/mai_tano/
# https://www.instagram.com/mai_tano/followers/

# "C:\00_BOX\chromedriver_win32\chromedriver.exe"

# https://qiita.com/memakura/items/20a02161fa7e18d8a693

import time
from selenium import webdriver
import requests
import json
import re

FETCH_COUNT = 20
MAX_COUNT = FETCH_COUNT * 2

TARGET_USER_ID = 'mai_tano'
GET_FOLLOWER_QUERY_HASH = 'c76146de99bb02f6415203be841dd25a'

INSTA_URL_HOME = 'https://www.instagram.com/'
INSTA_URL_REMEMBER_ME = INSTA_URL_HOME + 'accounts/onetap/?next=%2F'
INSTA_URL_TARGET_USER_PROFILE = INSTA_URL_HOME + TARGET_USER_ID

def button_click(button_text):
    buttons = driver.find_elements_by_tag_name("button")

    for button in buttons:
        if button.text == button_text:
            button.click()
            break

def createGetFollowerUrl(id,isAfter,endCursor):
    param = {
        "id" : id
        ,"include_reel" : False
        ,"fetch_mutual" : True
        ,"first" : FETCH_COUNT
    }

    if isAfter:
        param["after"] = endCursor
    return "https://www.instagram.com/graphql/query/?query_hash=" + GET_FOLLOWER_QUERY_HASH + "&variables=" + json.dumps(param)


driver = webdriver.Chrome('C:\\00_BOX\\selenium_driver\\chrome\\win\\83.0.4103.39\\chromedriver.exe')
driver.get(INSTA_URL_HOME)

time.sleep(5)

driver.find_element_by_name("username").send_keys('yyhhwork@gmail.com')
driver.find_element_by_name("password").send_keys('tesla12coil')
button_click("ログイン")
time.sleep(5)

if driver.current_url == INSTA_URL_REMEMBER_ME:
    button_click("後で")
    time.sleep(5)

session = requests.session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie["name"], cookie["value"])

driver.quit()

profileResult = session.get(INSTA_URL_TARGET_USER_PROFILE)
m = re.search('<script type="text\/javascript">window\._sharedData \= (.*?);<\/script>',profileResult.text)
profileDict = json.loads(m.group(1))
system_user_id = profileDict["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]

result = session.get(createGetFollowerUrl(system_user_id,False,None))
data = json.loads(result.text)

userNameList = [node["node"]["username"] for node in data["data"]["user"]["edge_followed_by"]["edges"]]
pageInfo = data["data"]["user"]["edge_followed_by"]["page_info"]
hasNext = pageInfo["has_next_page"]

while len(userNameList) < MAX_COUNT and hasNext:
    result2 = session.get(createGetFollowerUrl(system_user_id,True,pageInfo["end_cursor"]))
    data2 = json.loads(result2.text)
    userNameList2 = [node["node"]["username"] for node in data2["data"]["user"]["edge_followed_by"]["edges"]]
    pageInfo = data2["data"]["user"]["edge_followed_by"]["page_info"]
    hasNext = pageInfo["has_next_page"]
    userNameList.extend(userNameList2)

print(len(userNameList))
for userName in userNameList:
    print(userName)
