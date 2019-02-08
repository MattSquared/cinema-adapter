from json import load


class MapQuestAdapter:
    
    def __init__(self):
        configs = load(open("./mapquest/config.json"))
        self.__apikey = configs.get("apikey")
        self.__maproute = configs.get("maproute")
        self.__mapimage = configs.get("mapimage")
    
    
    def getRoute(self, start, end_x, end_y):
        position = start.split(";")
        start_x = position[0]
        start_y = position[1]
        map_route = self.__maproute.format(start_x, start_y, end_x, end_y)
        map_image = self.__mapimage.format(start_x, start_y, end_x, end_y, self.__apikey)
        result = {
            "cinemaroute": {
                "map_route": map_route,
                "map_image": map_image
            }
        }
        return result

