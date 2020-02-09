from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import os
import requests
import csv

app = Flask(__name__)
api = Api(app)

#Global Variables
file_downloaded = 0
iata_code = []
longitude = []
latitude = []

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
            iata_code.append(row[13])
            longitude.append(row[5])
            latitude.append(row[4])
    return

def get_data(code):
    iata_idx = iata_code.index(code)
    return iata_idx

#API Class Definitions
class Airports(Resource):

    def get(self, airport_code):
        download() #get the airports csv file
        read_data() #read all the airport codes in the file
        index = get_data(airport_code) #get the coordinates of the airport
        info = {iata_code[index]: [longitude[index], latitude[index]]}
        return info #return data to the user

#Resources
api.add_resource(Airports, '/<airport_code>')

if __name__ == '__main__':
    app.run()
