from pygeocoder import Geocoder
import pygeolib
import requests
import json
import logging as log
import difflib

wordstoremove = ['weather']


def weatherOnly(strin):
    words = strin.split()
    for word in words:
        if len(difflib.get_close_matches(word, wordstoremove, 3 , .6)) > 0:
            strin = strin.replace(word, "")
    return strin


def getWeather(strin):
    location = weatherOnly(strin).strip()
    if location == "":
        return "Invalid request. Please enter: weather followed by CITY,STATE (\"weather Madison,WI\")"
    log.info("Searching for location: " + location)
    try:
        result = Geocoder.geocode(location)
        (latitude, longitude) = result.coordinates
    except pygeolib.GeocoderError as e:
        # If over the query limit retry the request
        if e.status == "OVER_QUERY_LIMIT":
            log.info("OVER_QUERY_LIMIT Error thrown, retrying request")
            getWeather(strin)
            return;
        elif e.status == "ZERO_RESULTS":
            log.info("Invalid location requested returning error message")
            return "Invalid request. Please enter: weather followed by CITY,STATE (\"weather Madison,WI\")"
        else:
            log.info("Error thrown: " + e.status)
            return "Error: " + e.status

    # Request from DarkSky
    request = requests.get("https://api.darksky.net/forecast/{0}/{1},{2}".format("3d4089e5787a5054f02ef8fa4f348d2c",
                                                                                 latitude, longitude))
    #Load the json into an object
    data = json.loads(request.text)

    # Create final text to return
    finalText = "Forcast for the day:\n" + data['hourly']['summary']
    finalText += "\nCurrent Temperature: {0}".format(int(data['currently']['temperature'])) + u'\u00b0' + "F\n"
    finalText += "High Temperature: {0}".format(int(data['daily']['data'][0]['temperatureMax'])) + u'\u00b0' + "F\n"
    finalText += "Low Temperature: {0}".format(int(data['daily']['data'][0]['temperatureMin'])) + u'\u00b0' + "F"

    # If there is an alert add that to the final text
    if 'alert' in data:
        finalText += "\n" + data['alert']['title'] + "\n" + data['alert']['description']

    return finalText

