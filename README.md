# twitter-summarizer-snevarez1129

## Description
US Airports - Develop an API and module where we can get current conditions for the airport asked by the API and we can get current weather graphs (for example, the temperature for the last 24 hours) for specific period.  It does not have to be graphs but the data needed.

This API works by first downloading a CSV file from the internet. This file contains location and name data on all US airports. The API will get the name, IATA code, latitude, and longitude from the CSV file.

The API uses the latitude and longitude of the airport to call the openweathermap api to get current weather data for the airport. Temperature is measured in Kelvin.

Finally, the API again uses latitude and longitude of the airport to call the National Weather Service API to get temperature forecast for 24 hours. Temperature here is measured in Farenheit.

## Usage
(1) Create Python Virtual Environment

`python3 -m venv env`

`source env/bin/activate`

(2) Install Requirements

`pip3 install -r requirements.txt`

(3) Add API Keys - in the file api_dev.py, add your openweathermap API key to the variable API_KEY (line 15)

`API_KEY = ''`

(4) Start the Server

`python3 api_dev.py`

(5) Run the API either by IATA code or by airport name

`http://localhost:5000/iata/<airport_code>`

`http://localhost:5000/iata/<airport_name>`

## Response
This API returns a JSON object with the following parameters:
* id.name - airport name
* id.iata_code - airport iata code (not all airports have one)
* coord.latitude - airport latitude
* coord.longitude - airport longitude
* current_conditions.description - description of the current weather conditions
* current_conditions.feels_like - temperature it feels like it is outside
* current_conditions.actual_temp - acutal temperature in Kelvin
* current_conditions.pressure - pressure
* current_conditions.humidity - humidity
* forecast.time - hour
* forecast.temp - temperature in Farenheit
