from flask import Flask, request
from flask_restplus import Api, Resource
from movieglu import cinema_provider
from foursquare import venue_provider
from mapquest import map_provider
from utils import http_error


adapter_service = Flask(__name__)
api = Api(adapter_service)


''' Resource CinemaInfo is mapped to URI "/cinemainfo" '''
@api.route("/cinemainfo")
class CinemaInfo(Resource):
    def get(self):
        ''' GET method for retrieve CinemaInfo resource
            Headers:
                - geolocation: string containing the GPS position of the cinema
            Parameters: 
                - name: string containing the venue cinema
            Returns: JSON object containing the dataset if response is OK
        '''
        lat = request.headers.get("lat")
        lng = request.headers.get("lng")
        name = request.args.get("name")
        if not (lat and lng): 
            return http_error.missing_headers("lat, lng")
        if not name: 
            return http_error.missing_args("name")
        info = venue_provider.getVenueInfo(lat, lng, name)
        return info if info else http_error.not_found("name={}".format(name))


@api.route("/cinemaroute")
class CinemaRoute(Resource):
    def get(self):
        ''' GET method for retrieve CinemaRoute resource
            Headers:
                - geolocation: string containing the GPS position of the device
            Parameters: 
                - lat, lng: pairs of strings containing the cinema GPS position
            Returns: JSON object containing the dataset if response is OK
        '''
        geolocation = request.headers.get("geolocation")
        lat = request.args.get("lat")
        lng = request.args.get("lng")
        if not geolocation: 
            return http_error.missing_args("geolocation")
        if not (lat and lng): 
            return http_error.missing_args("lat, lng")
        route = map_provider.getRoute(geolocation, lat, lng)
        return route if route else http_error.not_found("lat={}, lng={}".format(lat, lng))


''' Resource Nearby is mapped to URI "/nearby" '''
@api.route("/nearby")
class Nearby(Resource):
    def get(self):
        ''' GET method for retrieve Nearby resource
            Headers:
                - geolocation: string containing geolocation data (GPS coordinates)
                - datetime: string containing datetime of the client device in ISO format
            Parameters: 
                - n (optional): integer representing the maximum number of cinemas to fetch
            Returns: JSON object containing the dataset if response is OK
        '''
        n = request.args.get("n")
        geolocation = request.headers.get("geolocation")
        datetime = request.headers.get("datetime")
        if not (geolocation and datetime): 
            return http_error.missing_headers("geolocation, datetime")
        nearby = cinema_provider.getNearby(geolocation, datetime, n)
        return nearby if nearby else http_error.not_found("nearby")


''' Resource Showtimes is mapped to URI "/showtimes" '''
@api.route("/showtimes")
class Showtimes(Resource):
    def get(self):
        ''' GET method for retrieve Showtimes resource
                Headers:
                    - geolocation: string containing geolocation data (GPS coordinates)
                    - datetime: string containing datetime of the client device in ISO format
                Parameters:
                    - cinema_id: string containing the cinema ID
                    - date: string containing the date in YYYY-MM-DD format
                Returns: JSON object containing the dataset if response is OK
            '''
        cinema = request.args.get("cinema_id")
        date = request.args.get("date")
        geolocation = request.headers.get("geolocation")
        datetime = request.headers.get("datetime")
        if not (geolocation and datetime): 
            return http_error.missing_headers("geolocation, datetime")
        if not (cinema and date): 
            return http_error.missing_args("cinema_id, date")
        showtimes = cinema_provider.getShowtimes(geolocation, datetime, cinema, date)
        return showtimes if showtimes else http_error.not_found("cinema_id={}, date={}".format(cinema, date))



if __name__ == "__main__":
    adapter_service.run()
