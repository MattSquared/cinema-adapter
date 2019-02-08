# Cinema Adapter Service
## Description
This service acts as an interface between the Business Logic service and providers such as **MovieGlu**, **FourSquare** and **MapQuest**.
The service is a web application implemented in Python by using **Flask** framework and its extension called **Flask-RESTplus**.  
The service relies on:  

- **MovieGlu** to access information about nearby cinemas and their showtimes according to the user GPS location.
- **FourSquare** to retrieve information about cinemas as places, like phone number and social network contacts.
- **MapQuest** to retrieve a map where the cinema is located and a link to the route explaination.

## Modules
- **AdapterService**: implements a Flask application for managing requests to MovieGlu, MapQuest and FourSquare resources.
- **MovieGluAdapter**: class that wraps methods for quering MoviesGlu.
- **FourSquareAdapter**: class that wraps methods for querying FourSquare.
- **MapQuestAdapter**: class that wraps methods for querying MapQuest.

## References
### Flask
- Flask: [http://flask.pocoo.org/](http://flask.pocoo.org/)
- Flask-RESTplus: [https://flask-restplus.readthedocs.io/en/stable/index.html](https://flask-restplus.readthedocs.io/en/stable/index.html)

### MovieGlu
- MovieGlu: [https://www.movieglu.com/](https://www.movieglu.com/)
- MovieGlu APIs: [https://developer.movieglu.com/](https://developer.movieglu.com/)

### FourSquare
- FourSquare: [https://foursquare.com/](https://foursquare.com/)
- FourSquare APIs: [https://developers.foursquare.com/]([https://developers.foursquare.com/])

### MapQuest
- MapQuest: [https://www.mapquest.com](https://www.mapquest.com)
- MapQuest APIs: [https://developer.mapquest.com](https://developer.mapquest.com)
