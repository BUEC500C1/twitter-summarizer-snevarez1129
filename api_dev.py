from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import os
import requests


app = Flask(__name__)
api = Api(app)


airports = {}
longitude = {}
latitude = {}

def download():
    global file_downloaded
    if file_downloaded == 0:
        #download file from the internet
        url = 'http://ourairports.com/data/airports.csv'
        response = requests.get(url)
        with open(os.path.join("/Users/sebastiannevarez/Desktop/EngEc500/twitter-summarizer-snevarez1129", "file.csv"), 'wb') as airports:
            airports.write(response.content)
        #set the download flag
        file_downloaded = 1
    return

file_downloaded = 0

class Airports(Resource):
    def get(self, airport_code):
        
        #get the airports csv file
        download()
        print("done?")

        #read all the airport codes in the file
        #get the coordinates of the airport

        #return data to user        
        return {'airport_code': 'longitude'}

#api.add_resource(HelloWorld, '/')
api.add_resource(Airports, '/<airport_code>')

if __name__ == '__main__':
    app.run()
