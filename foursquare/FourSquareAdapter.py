from json import load
from jsonbender import bend, OptionalS
from utils import http_request


class FourSquareAdapter:
    ''' This class wraps methods for request resources from FourSquare
        Exposed methods:
            > getVenueInfo(): given the venue GPS location and its name, it finds information about it
    '''
    
    def __init__(self):
        ''' Constructor of the class
            Attributes:
                * __server: address of the endpoint where perform requests
                * __headers: map of headers for HTTP requests to Foursquare APIs
                * __request: HttpRequest instance for performing HTTP request
        '''
        configs = load(open("./foursquare/config.json", "r"))
        self.__server = configs.get("server")
        self.__mandatory = configs.get("headers")
    
    
    def __filterId(self, dataset):
        ''' Private method for fetch venue id from dataset '''
        mapping = {"id": OptionalS("response", "venues", 0, "id")}
        return bend(mapping, dataset)
    
    
    def __filterInfo(self, dataset):
        ''' Private method for fetch venue contacts from dataset '''
        mapping = { 
            "contact": {
                "phone": OptionalS("response", "venue", "contact", "formattedPhone"),
                "instagram": OptionalS("response", "venue", "contact", "instagram"),
                "twitter": OptionalS("response", "venue", "contact", "twitter"),
                "facebook": OptionalS("response", "venue", "contact", "facebookUsername")
            },
            "url": OptionalS("response", "venue", "url")
        }
        return bend(mapping, dataset)
    
    
    def __filterHours(self, dataset):
        ''' Private method for fetch venue opening hours from dataset '''
        mapping = {
            "hours": OptionalS("response", "hours", "timeframes"),
            "popular": OptionalS("response", "popular", "timeframes")
        }
        bending = bend(mapping, dataset)
        result = {"hours": None}
        framesList = []
        if bending.get("hours"): framesList = bending.get("hours")
        if bending.get("popular"): framesList = bending.get("popular")
        if framesList:
            daysMapping = {1:"Mon", 2:"Tue", 3:"Wed", 4:"Thu", 5:"Fri", 6:"Sat", 7:"Sun"}
            time_format = lambda time: "{}:{}".format(time[:2], time[2:]) if not time.startswith('+') else "00:00"
            timeFrames = [""] * 7
            for frame in framesList:
                days,openings = frame.get("days"), frame.get("open")
                hours = ", ".join(["{}-{}".format(time_format(time["start"]), time_format(time["end"])) for time in openings])
                for index in days: timeFrames[index-1] = "{}: {}".format(daysMapping.get(index), hours)
            result.update({"hours": timeFrames})
        return result
    
    
    def __fetchVenueId(self, ll, query, limit=1):
        ''' Method for retrieve the venue ID
            Arguments:
                - ll: string containing the GPS position of the venue
                - query: string containing the venue name
                - limit (optional): set maximum number of items to fetch
            Returns: integer containing the ID for the venue, otherwise None (null object)
        '''
        uri = "search"
        params = self.__mandatory
        params.update({"ll": ll, "query": query, "limit": limit})
        params.update({"categoryId": "4bf58dd8d48988d17f941735", "intent": "checkin"})
        result = http_request.get(self.__server, uri, params=params)
        if result: 
            return self.__filterId(result)
    
    
    def __fetchVenueInfo(self, venueId):
        ''' Method for retrieve information about the venue
            Arguments:
                - venueId: string containing the venue ID
            Returns: dictionary object containing information about the venue, otherwise None (null object)
        '''
        uri = venueId
        result = http_request.get(self.__server, uri, params=self.__mandatory)
        if result: 
            return self.__filterInfo(result)
    
    
    def __fetchVenueHours(self, venueId):
        ''' Method for retrieve information about the venue
            Arguments:
                - venueId: string containing the venue ID
            Returns: dictionary object containing the venue's opening hours, otherwise None (null object)
        '''
        uri = "{}/hours".format(venueId)
        result = http_request.get(self.__server, uri, params=self.__mandatory)
        if result: 
            return self.__filterHours(result)
    
    
    def getVenueInfo(self, lat, lng, query):
        ''' Method for retrieve information and opening hours of a venue
            Arguments:
                - lat, lng: pair of 2 strings containing the GPS position of the venue
                - name: string containing the venue name
            Return: filtered JSON object if HTTP response is OK, otherwise None (null object)
        '''
        position = "{},{}".format(lat, lng)
        name = query.replace("-", "")
        venue = self.__fetchVenueId(position, name)
        venueId = venue.get("id")
        if not venueId: 
            return
        info = self.__fetchVenueInfo(venueId)
        hours = self.__fetchVenueHours(venueId)
        if info and hours: 
            result = {"cinemainfo": {**info, **hours}}
            return result

