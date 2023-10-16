from flask import Flask, jsonify, abort, request
import requests
import argparse
import json

from clients import GeocodioClient, YelpClient
from constants import geocodio_key, yelp_key
app = Flask(__name__)

geocodio_api_key = geocodio_key
geocodio_client = GeocodioClient(geocodio_api_key)

yelp_api_key = yelp_key
yelp_client = YelpClient(yelp_api_key)


@app.route('/restaurant/<restaurant_addr>', methods=['GET'])
def restaurant(restaurant_addr):
    if request.method == 'GET':
        address = restaurant_addr
        print("Address parameter:", address)
        geocoding_result = geocodio_client.request(address)
        if geocoding_result is not None:
            lat, lon = geocoding_result
            if lat is not None and lon is not None:
                yelp_response = yelp_client.request(lat, lon)
                if yelp_response is not None:
                    # yelp_status_code = yelp_response.get("code")
                    # if(yelp_status_code != 200):
                    #     abort(500, f"Yelp API request failed with status code {yelp_status_code}")
                            
                    formatted_restaurants = [
                            {
                                "name": restaurant["name"],
                                "address": restaurant["location"]["address1"],
                                "rating": str(restaurant["rating"])
                            }
                        for restaurant in yelp_response.get("businesses",[])
                        ]
                    return jsonify({"restaurants" : formatted_restaurants})
        else:
            return jsonify({"error": "Geocoding request failed or no results found"})

    


##########################
# Do **NOT** remove this.
def parse_args():
    parser =argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000,
                        help='port number.')
    return parser.parse_args()

if __name__ == '__main__': 
    args = parse_args()
    app.run(port=args.port)