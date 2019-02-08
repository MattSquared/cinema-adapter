from json import load
from utils import http_request


class MovieGluAdapter:
    ''' This class wraps methods for request resources from MoviesGlu
        Exposed methods:
            > getNearby(): given GPS location, retrieves the list of nearby cinemas
            > getShowtimes(): given a cinema ID and a date, retrieves the shotimes for the wanted date 
    '''
    
    def __init__(self):
        ''' Constructor of the class
            Attributes:
                * __server: address of the endpoint where perform requests
                * __headers: map of headers for HTTP requests to MovieGlu APIs
        '''
        configs = load(open("./movieglu/config.json", "r"))
        self.__server = configs.get("server")
        self.__headers = configs.get("headers")
    
    
    def __filterNearby(self, dataset):
        ''' Private method for filtering Nearby dataset '''
        filters = ["cinema_id", "cinema_name", "address", "city", "lat", "lng"]
        return {"cinemas": [{key:value for key,value in cinema.items() if key in filters} for cinema in dataset.get("cinemas")]}
    
    
    def __filterShowtimes(self, dataset):
        ''' Private method for filtering Showtimes dataset '''
        imdb_id_format = lambda value: "tt{}".format(str(value).zfill(7))
        propertiesFilters = ["film_id", "film_name"]
        showtypeFilters = ["Standard", "3D"]
        films = []
        for properties in dataset.get("films"):
            if properties.get("imdb_id") != "0": 
                film = {}
                for key,value in properties.items():
                    if key in propertiesFilters: film[key] = value
                    if key == "imdb_id": film[key] = imdb_id_format(value)
                    if key == "showings": film[key] = {showtype.lower():[time.get("start_time") for time in times.get("times")] for showtype,times in value.items() if showtype in showtypeFilters}
                    if key == "show_dates": film[key] = [date.get("date") for date in value]
                films.append(film)
        return {"films": films}
    
    
    def getNearby(self, geolocation, datetime, n=None):
        ''' Method for retrieve a list of nearby cinemas
            Arguments:
                - geolocation: string containing geolocation data (GPS coordinates)
                - datetime: string containing datetime of the client device in ISO format
                - n (optional): integer representing the maximum number of items to fetch
            Return: filtered JSON object if HTTP response is OK, otherwise None (null object)
        '''
        uri = "cinemasNearby/"
        headers = {"geolocation": geolocation, "device-datetime": datetime}
        headers.update(self.__headers)
        params = {"n": 5}
        if n: params.update({"n": n})
        result = http_request.get(self.__server, uri, headers, params)
        if result: 
            return self.__filterNearby(result)
    
    
    def getShowtimes(self, geolocation, datetime, cinema, date):
        ''' Method for retrieve the showtimes in a date for a given cinema
            Arguments:
                - geolocation: string containing geolocation data (GPS coordinates)
                - datetime: string containing datetime of the client device in ISO format
                - cinema: string containing the cinema ID
                - date: string containing the date in YYYY-MM-DD format
            Return: filteredJSON object if HTTP response is OK, otherwise None (null object)
        '''
        uri = "cinemaShowTimes/"
        headers = {"geolocation": geolocation, "device-datetime": datetime}
        headers.update(self.__headers)
        params = {"cinema_id": cinema, "date": date}
        result = http_request.get(self.__server, uri, headers, params)
        if result: 
            return self.__filterShowtimes(result)

