# twitter-summarizer-snevarez1129

US Airports - Develop an API and module where we can get current conditions for the airport asked by the API and we can get current weather graphs (for example, the temperature for the last 24 hours) for specific period.  It does not have to be graphs but the data needed.

This API works by first downloading a CSV file from the internet. This file contains location and name data on all US airports. The API will get the name, IATA code, latitude, and longitude from the CSV file.

The API uses the latitude and longitude of the airport to call the openweathermap api to get current weather data for the airport. Temperature is measured in Kelvin.

Finally, the API again uses latitude and longitude of the airport to call the National Weather Service API to get temperature forecast for 24 hours. Temperature here is measured in Farenheit.
