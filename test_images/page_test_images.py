import time
import requests
import re

# page_url = input("Page URL: ")
# new_cdn = input("New CDN path: ")
page_url = "https://sputniknews.vn/"
new_cdn = "cdn1.img.sputniknews.vn"
response = requests.get(page_url)
if response.status_code != 200:
    print ("ERROR: The page cannot be loaded!")
    exit()
source = response.text
# Domain of the page
domain = (re.search("^https://([A-Za-z_0-9.-]+).*", page_url)).group(1)
# The regular expression for select CDN part
regexp_cdn_domain = "cdn\d.img." + domain + "/?([^<?\'\\\" >]+)"
links_list = []
links_list = re.findall(regexp_cdn_domain, source)
newcdn_links_list = []
for l in links_list:
    newcdn_links_list.append("https://" + new_cdn + "/" + l)
n_all = 0
n_err = 0
for l in newcdn_links_list:
    response_image = requests.get(l)
    status = response_image.status_code
    n_all += 1
    if status != 200:
        print(l, "   |   ", status)
        n_err += 1
print ("Errors {0:d} from {1:d} urls ({2:.1f}%)".format(n_err, n_all, (n_err/n_all)*100))


