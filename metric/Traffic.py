import requests
import json
import datetime

class Traffic:
    def __init__(self):
    # Определяем параметры запросов
        with open('config.json') as json_file:
             all_conf = json.load(json_file)
             self.config = all_conf['init_parameters']
             self.login = self.config['login']
             self.password = self.config['password']
             self.token = self.config['token']
             self.cdnnow_url = self.config['url']
             self.metrics = self.config["metrics"]
             self.group_by = self.config["group_by"]
             self.filter_by = self.config["filter_by"]
             self.dates = all_conf['dates']
             self.from_date = self.dates['from']
             self.to_date = self.dates['to']
        # Коды разбиения статистики, в значениях - секунды
        self.granularity = {
            60: "PT1M",
            300: "PT5M",
            600: "PT10M",
            1200: "PT20M",
            1800: "PT30M",
            3600: "PT1H",
            7200: "PT2H",
            18000: "PT5H",
            36000: "PT10H",
            72000: "PT20H",
            86400: "P1D"
        }
        # Результирующее число точек, которое определятся как разница между from/to деленое на granularity не должно превышать 1440.
        self.max_point = 1440

    def granula(self, tfrom:datetime, tto:datetime, param=True):
        # Определяется параметр granularity
        dift = tto - tfrom
        difsec = dift.total_seconds()
        # Если параметр True прибавляем секунды за одни сутки 
        if param == True:
            difsec += 3600 * 24
        gran_seconds = self.granularity.keys()
        choose_gran = False
        result = ""
        for sec in gran_seconds:
            if (difsec/sec) <= self.max_point:
                choose_gran = True
                result = self.granularity.get(sec)
                return result
        # Проверка, что максимальное разбиение не будет превышать допустимое
        if choose_gran == False and (difsec/gran_seconds[len(gran_seconds) - 1]) > self.max_point:
            print ("ERROR: Too large range between from and to dates (" + str(difsec) + " seconds)")
            return False
        else:
            result = self.granularity.get(gran_seconds[len(gran_seconds) - 1])
            return result

    def get_traffic_metric(self, project):
        # формируем даты начала и конца статистики
        date_from = datetime.date(int(self.from_date[0]), int(self.from_date[1]), int(self.from_date[2]))
        date_to = datetime.date(int(self.to_date[0]), int(self.to_date[1]), int(self.to_date[2]))
        if self.granula(date_from, date_to) != False:
            granula = self.granula(date_from, date_to)
        ((self.filter_by)[0]).update({"values": [project]})
        request_data = {
            "metrics": self.metrics,
            "from": date_from.isoformat() + "T00:00:00Z",
            "to": date_to.isoformat() + "T23:59:59Z",
            "granularity": granula,
            "filter_by": self.filter_by,
            "group_by": self.group_by
        }
        # print (request_data)
        response = requests.post(self.cdnnow_url, headers={"x-auth-token": self.token}, json=request_data)
        if response.status_code == 200:
            return (response.json())["data"][project]
        else:
            print ("ERROR: code - ", response.status_code, " ", response.text)
            return False
    