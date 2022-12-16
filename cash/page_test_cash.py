import time
from Test_Cash import Test_Cash
import requests
import re
import random

page_url = input("Page URL:")
response = requests.get(page_url)
if response.status_code != 200:
    print ("ERROR: The page cannot be loaded!")
    exit()
source = response.text
domain = (re.search("^https://([A-Za-z_0-9.-]+).*", page_url)).group(1)
regexp_cdn_domain = "cdn\d.img." + domain + "/?([^<?\'\\\" >]+)"
links = []
links_list = re.findall(regexp_cdn_domain, source)
lenlist = len(links_list)
if lenlist == 0:
    print ("ERROR: CDN content was not be found on the page!")
    exit()
elif lenlist > 0 and lenlist <= 10:
    links = links_list.copy()
elif lenlist > 10:
    random.seed()
    i = 0
    choose_list = []
    while i < 10:
        new_n = True
        while new_n:
            n = random.randrange(0, lenlist)
            if choose_list.count(n) == 0 and (links_list[n]).endswith("/") == False:
                choose_list.append(n)
                i += 1
                new_n = False
    for k in range(0, 10):
        links.append(links_list[choose_list[k]])

objTest = Test_Cash(domain)
if objTest.get_token() != False:
    token = objTest.get_token()
    print ("Token:", token)
    print ("Check job status")
    while objTest.get_status(token) == False:
        time.sleep(1)
        print ("-", end='', flush=True)
    if objTest.test_link(token, links):
        print ("Start testing")
        time.sleep(5)
        while objTest.check_test_status(token) != "passed":
            print (">", end='', flush=True)
            time.sleep(5)
        print ("")
        results = objTest.get_test_result(token)
        for key, values in results.items():
            for i in values:
                print(key, " : ", i.items())
        objTest.terminate_test(token)

