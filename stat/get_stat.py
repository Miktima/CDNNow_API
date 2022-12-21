from Stat import Stat
import requests
import re
import matplotlib.pyplot as plt

page_url = input("Page URL:")
response = requests.get(page_url)
if response.status_code != 200:
    print ("ERROR: The page cannot be loaded!")
    exit()
source = response.text
domain = (re.search("^https://([A-Za-z_0-9.-]+).*", page_url)).group(1)
objStat = Stat(domain)
if objStat.get_token() != False:
    token = objStat.get_token()
    print ("Token:", token)
    response = objStat.get_stat(token)
    if response != False:
        plot_y = []
        plot_x = []
        for key, value in response.items():
            f = (list(value.values()))[0]
            plot_y.append(f)
            plot_x.append(key)
            print (key + " - " + str(f))        
        # plt.plot(plot_x, plot_y)
        plt.plot(plot_x, plot_y)
        plt.ylabel('TB')
        plt.show()