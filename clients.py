import requests
import json

class GeocodioClient(object):
    """
    The client that makes request to the Geocodio 
    to get the corresponding (latitude, longitude) pair. 
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.geocod.io/v1.7/geocode"

    def request(self, addr):
        formatted_address = addr.replace(" ", "-")
        params= {
            'q': formatted_address,
            'api_key': self.api_key
        }
        response = requests.get(self.base_url, params = params)
        if(response.status_code == 200):
            geocoded_data = response.json()
            if 'results' in geocoded_data and geocoded_data['results']:
                lat = geocoded_data['results'][0]['location']['lat']
                lon = geocoded_data['results'][0]['location']['lng']
                return lat, lon
            else:
                return None
        else:
            return None
    


class YelpClient(object):
    """
    The client that makes request to the Yelp
    to get a list of nearby restaurants.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.yelp.com/v3/businesses/search"

    def request(self, latitude, longitude):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "categories": "food"
        }
        response = requests.get(self.base_url, headers = headers,params = params)
        
        if response.status_code == 200:
            yelp_data = response.json()
            return yelp_data
        else:
            return None