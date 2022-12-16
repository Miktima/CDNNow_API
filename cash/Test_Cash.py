import requests
import json

class Test_Cash:
    def __init__(self, portal):
    # Определяем параметры запросов
        with open('config.json') as json_file:
             all_conf = json.load(json_file)
             self.config = all_conf['init_parameters']
             self.login = self.config['login']
             self.password = self.config['password']
             self.cdnnow_urlauth = self.config['url_auth']
             self.cdnnow_url_status = self.config['url_status']
             self.cdnnow_url_request = self.config['url_request']
             self.portals = all_conf['portals']
             self.id_portal = self.portals[portal]
        
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
    
    def get_status(self, token):
        # Статус сервиса для отправки запроса в API
        url = (self.cdnnow_url_status).replace("##portal##", self.id_portal)
        response = requests.get(url, headers = {'token': token})
        if (response.json())["runstate"] == "busy":
            return False
        elif (response.json())["runstate"] == "available":
            return True
    
    def test_link(self, token, list_link:list):
        # Формируем запрос для проверки надбора линков
        links = {}
        links.update({"paths" : list_link})
        url = (self.cdnnow_url_request).replace("##portal##", self.id_portal)
        response = requests.post(url, headers = {'token': token}, json = links)
        if response.status_code == 202:
            return True
        else:
            print ("ERROR: response:", response)
            # print ("URL:", url)
            # print ("Links:", links["paths"])
            return False
    
    def check_test_status(self, token):
        # Проверка статуса выполнения задачи: "pending", "running", "passed"
        url = (self.cdnnow_url_request).replace("##portal##", self.id_portal)
        response = requests.get(url, headers = {'token': token})
        return (response.json())["status"]
    
    def get_test_result(self, token) -> json:
        # Получаем результат и возвращаем его
        # Массив результатов проверки каждого URL-пути. Ключ содержит URL-путь, значение - поля:
        #   "checked" - boolean, завершена (true) или выполняется (false) проверка данного URL-пути,
        #   "errors"  - строковый массив, содержащий текстовые сообщения об ошибках проверки.
        url = (self.cdnnow_url_request).replace("##portal##", self.id_portal)
        response = requests.get(url, headers = {'token': token})
        if (response.json())["status"] == "passed":
            return (response.json())["paths"]
    
    def terminate_test(self, token):
        # Завершает либо прерывает текущую задачу, освобождая сервис для следующих запросов.
        url = (self.cdnnow_url_request).replace("##portal##", self.id_portal)
        requests.delete(url, headers = {'token': token})
