from json import load
import requests


class HttpRequest:
    def __init__(self):
        configs = load(open("./utils/config.json"))
        self.__fs = configs.get("repository").get("foursquare")
        self.__mg = configs.get("repository").get("movieglu")
    
    
    def __jsonRequest(self, resource, headers=None, params=None):
        jsonfile = None
        if resource == "cinemasNearby/": jsonfile = "{}/cinemasNearby/{}.json".format(self.__mg, headers.get("geolocation"))
        elif resource == "cinemaShowTimes/": jsonfile = "{}/cinemaShowTimes/{}.json".format(self.__mg, params.get("cinema_id"))
        elif resource == "search": jsonfile = "{}/search_{}.json".format(self.__fs, params.get("query"))
        else: jsonfile = "{}/{}.json".format(self.__fs, resource)
        if jsonfile: return load(open(jsonfile))
    
    
    def get(self, server, uri, headers=None, params=None):
        url = "{}{}".format(server, uri)
        try:
            response = requests.get(url=url, headers=headers, params=params)
            if response.status_code == requests.codes.get("ok"):
                return response.json()
            else:
                return self.__jsonRequest(uri, headers, params)
        except:
            return self.__jsonRequest(uri, headers, params)

