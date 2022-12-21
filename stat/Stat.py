import requests
import json

class Stat:
    def __init__(self, portal):
    # Определяем параметры запросов
        with open('config.json') as json_file:
             all_conf = json.load(json_file)
             self.config = all_conf['init_parameters']
             self.login = self.config['login']
             self.password = self.config['password']
             self.id_client = self.config['client_id']
             self.cdnnow_urlauth = self.config['url_auth']
             self.cdnnow_urlstat = self.config['url_stat']
             self.portals = all_conf['portals']
             self.id_portal = self.portals[portal]
             self.date = all_conf['date']
             self.year = self.date['year']
             self.month = self.date['month']
             self.day = self.date['day']
        
    def get_token(self):
        # Получаем токен для последующих запросов
        login_data = {
            'username': self.login,
            'password': self.password
        }
        response = requests.post(self.cdnnow_urlauth, data = login_data)
        if (response.json())["status"] != "ok":
            print ("ERROR: response status:", response.json())
            return False
        else:
            data = (response.json())["data"]
            return data["token"]
    
    def get_stat(self, token):
        # получаем статистику за день, если указан день, или за месяц, если день не указан
        request_data = {
            "token": token,
            "year": int(self.year),
            "month": int(self.month),
            "client": self.id_client,
            "project": self.id_portal
        }
        if len(self.day) > 0:
            request_data.update({"day": int(self.day)})
        response = requests.get(self.cdnnow_urlstat, params = request_data)
        if response.status_code == 200:
            return (response.json())["data"]["data"]
        else:
            print ("Request URL: ", response.url)
            print ("ERROR: code - ", response.status_code)
            return False
    