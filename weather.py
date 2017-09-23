from pygeocoder import Geocoder
import requests
import json


def getweather(location):

    result = Geocoder.geocode(location)
    (latitude, longitude) = result.coordinates
    request = requests.get("https://api.darksky.net/forecast/{0}/{1},{2}".format("3d4089e5787a5054f02ef8fa4f348d2c",
                                                                                 latitude, longitude))
    data = json.loads(request.text)
    print(data["hourly"]["summary"])

