from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import os
import requests
import csv

app = Flask(__name__)
api = Api(app)

#Global Variables
airport_name = [] #list of available airport names
iata_code = [] #list of iata codes
latitude = [] #list of latitudes
longitude = [] #list of longitudes
API_KEY = '' #api key for openweathermap api
description = "" #description of the current weather conditions
feels_like = "" #temperature it feels like outside in Kelvin
actual_temp = "" #temperature it acutally is outside in Kelvin
pressure = "" #pressure
humidity = "" #humidity
forecast_time = [] #list of 24hrs
forecast_temp = [] #list of forecast temps for 24hrs

#Modular Funciton Definitions
def download():
    #download csv file from the internet
    url = 'http://ourairports.com/data/airports.csv'
    response = requests.get(url)
    with open(os.path.join("/Users/sebastiannevarez/Desktop/EngEc500/twitter-summarizer-snevarez1129", "airport_data.csv"), 'wb') as myfile:
        myfile.write(response.content)
    return

def load_data():
    try:
        #if the file already exists
        with open('airport_data.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                airport_name.append(row[3])
                iata_code.append(row[13])
                latitude.append(row[4])
                longitude.append(row[5])
    except IOError:
        #if it is not already downloaded
        download() #download the airports csv file
        #and then open it and get the data
        with open('airport_data.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                airport_name.append(row[3])
                iata_code.append(row[13])
                latitude.append(row[4])
                longitude.append(row[5])
    finally:
        return

def get_data(code):
    iata_idx = iata_code.index(code) #find the index of the iata code in the list
    return iata_idx

def get_data_by_name(name):
    fixed_name = name.replace('-', ' ') #get rid of - in the name
    name_idx = airport_name.index(fixed_name) #find the index of the airport name in the list
    return name_idx

def get_weather(lat, lon):
    #get the current weather data from openweatherapi
    global API_KEY
    URL = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + str(API_KEY)
    response = requests.get(URL).json()
    return response

def read_weather(json_data):
    global description
    description = json_data['weather'][0]['description'] #save the description
    global feels_like
    feels_like = json_data['main']['feels_like'] #save what it feels like
    global actual_temp
    actual_temp = json_data['main']['temp'] #save the actual temperature
    global pressure
    pressure = json_data['main']['pressure'] #save the pressure
    global humidity
    humidity = json_data['main']['humidity'] #save the humidity
    return

def get_temp_data(lat, lon):
    #get forecast data from the national weather service api
    global forecast_time
    global forecast_temp
    URL = "https://api.weather.gov/points/" + str(lat) + "," + str(lon)
    response = requests.get(URL).json()
    forecast_url = response['properties']['forecastHourly']
    new_response = requests.get(forecast_url).json()
    #for 24 hours
    i = 0
    while i < 24:
        forecast_time.append(new_response['properties']['periods'][i]['startTime']) #save the times
        forecast_temp.append(new_response['properties']['periods'][i]['temperature']) #save the temperatures
        i += 1
    return

def format_response(index):
    #format the api response in JSON format
    data = {
        'id': {
            'name': airport_name[index],
            'iata_code': iata_code[index]
        },
        'coord': {
            'latitude': latitude[index],
            'longitude': longitude[index]
        },
        'current_conditions': {
            'description': description,
            'feels_like': feels_like,
            'actual_temp': actual_temp,
            'pressure': pressure,
            'humidity': humidity
        },
        'forecast': [
            {
                'time': forecast_time[0],
                'temp': forecast_temp[0]
            },
            {
                'time': forecast_time[1],
                'temp': forecast_temp[1]
            },
            {
                'time': forecast_time[2],
                'temp': forecast_temp[2]
            },
            {
                'time': forecast_time[3],
                'temp': forecast_temp[3]
            },
            {
                'time': forecast_time[4],
                'temp': forecast_temp[4]
            },
            {
                'time': forecast_time[5],
                'temp': forecast_temp[5]
            },
            {
                'time': forecast_time[6],
                'temp': forecast_temp[6]
            },
            {
                'time': forecast_time[7],
                'temp': forecast_temp[7]
            },
            {
                'time': forecast_time[8],
                'temp': forecast_temp[8]
            },
            {
                'time': forecast_time[9],
                'temp': forecast_temp[9]
            },
            {
                'time': forecast_time[10],
                'temp': forecast_temp[10]
            },
            {
                'time': forecast_time[11],
                'temp': forecast_temp[11]
            },
            {
                'time': forecast_time[12],
                'temp': forecast_temp[12]
            },
            {
                'time': forecast_time[13],
                'temp': forecast_temp[13]
            },
            {
                'time': forecast_time[14],
                'temp': forecast_temp[14]
            },
            {
                'time': forecast_time[15],
                'temp': forecast_temp[15]
            },
            {
                'time': forecast_time[16],
                'temp': forecast_temp[16]
            },
            {
                'time': forecast_time[17],
                'temp': forecast_temp[17]
            },
            {
                'time': forecast_time[18],
                'temp': forecast_temp[18]
            },
            {
                'time': forecast_time[19],
                'temp': forecast_temp[19]
            },
            {
                'time': forecast_time[20],
                'temp': forecast_temp[20]
            },
            {
                'time': forecast_time[21],
                'temp': forecast_temp[21]
            },
            {
                'time': forecast_time[22],
                'temp': forecast_temp[22]
            },
            {
                'time': forecast_time[23],
                'temp': forecast_temp[23]
            }
        ]
    }
    return data

#API Class Definitions
class Name(Resource):
    def get(self, port_name):
        load_data() #load all the airports in the file
        index = get_data_by_name(port_name) #get the coordinates of the airport
        res = get_weather(latitude[index], longitude[index]) #get weather based on coordinates using openweathermap api
        read_weather(res) #get the data we want from the api response
        get_temp_data(latitude[index], longitude[index]) #get forecast for next 24hrs
        data = format_response(index) #format api response
        return data, 202 #return data to the user

class IATA(Resource):
    def get(self, airport_code):
        load_data() #load all the airports in the file
        index = get_data(airport_code) #get the coordinates of the airport
        res = get_weather(latitude[index], longitude[index]) #get weather based on coordinates using openweathermap api
        read_weather(res) #get the data we want from the api response
        get_temp_data(latitude[index], longitude[index]) #get forecast for next 24hrs
        data = format_response(index) #format api response
        return data, 201 #return data to the user

#Resources
api.add_resource(IATA, '/iata/<airport_code>') #user can call with iata code
api.add_resource(Name, '/name/<port_name>') #user can call with airport name

if __name__ == '__main__':
    app.run()
