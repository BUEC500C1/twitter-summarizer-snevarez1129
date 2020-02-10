from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import os
import requests
import csv

app = Flask(__name__)
api = Api(app)

#Global Variables
file_downloaded = 0
name = []
iata_code = []
latitude = []
longitude = []
API_KEY = ''
description = ""
feels_like = ""
actual_temp = ""
pressure = ""
humidity = ""

#Modular Funciton Definitions
def download():
    global file_downloaded #define global variable
    if file_downloaded == 0: #if we haven't downloaded the file yet
        #download file from the internet
        url = 'http://ourairports.com/data/airports.csv'
        response = requests.get(url)
        with open(os.path.join("/Users/sebastiannevarez/Desktop/EngEc500/twitter-summarizer-snevarez1129", "airport_data.csv"), 'wb') as myfile:
            myfile.write(response.content)
        file_downloaded = 1 #set the download flag
    return

def read_data():
    with open('airport_data.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            name.append(row[3])
            iata_code.append(row[13])
            latitude.append(row[4])
            longitude.append(row[5])
    return

def get_data(code):
    iata_idx = iata_code.index(code)
    return iata_idx

def get_weather(lat, lon):
    global API_KEY
    URL = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + str(API_KEY)
    response = requests.get(URL).json()
    return response

def read_weather(json_data):
    global description
    description = json_data['weather'][0]['description']
    global feels_like
    feels_like = json_data['main']['feels_like']
    global actual_temp
    actual_temp = json_data['main']['temp']
    global pressure
    pressure = json_data['main']['pressure']
    global humidity
    humidity = json_data['main']['humidity']
    return

#API Class Definitions
class Airports(Resource):
    def get(self, airport_code):
        #download() #get the airports csv file
        read_data() #read all the airport codes in the file
        index = get_data(airport_code) #get the coordinates of the airport
        res = get_weather(latitude[index], longitude[index]) #get weather based on coordinates using openweathermap api
        read_weather(res) #get the data we want from the api response
        info = {iata_code[index]: [latitude[index], longitude[index]]}
        return info, 201 #return data to the user

# class CurrentWeather(Resource):
#     def get(self, lon, lat):
#         res = get_weather(lon, lat)
#         print(res)
#         return

#Resources
api.add_resource(Airports, '/<airport_code>')
#api.add_resource(CurrentWeather, '/<lon>/<lat>')

if __name__ == '__main__':
    app.run()
