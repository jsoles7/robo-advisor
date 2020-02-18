# app/robo_advisor.py

#import certain modules/ packages
import requests
import json 
from datetime import datetime

#defining key variables
now = datetime.now()

#defining applicable functions for main program
#to_usd function adapted from that one given/ developed by Professor Rossetti
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


#scrapping what is required from web 
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)

print(response.status_code) #> 200
#print(response.text)

#parse from the response text into dictionary
parsed_response = json.loads(response.text)
#print(parsed_response)
latest_refresh = parsed_response["Meta Data"]["3. Last Refreshed"]


#establishing output variables
time_series_keys = list(parsed_response["Time Series (Daily)"].keys())
latest_day_applicable = time_series_keys[0]
latest_close = parsed_response["Time Series (Daily)"][latest_day_applicable]["4. close"]

#receiving client inputs
 


#Program outputs
print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print("LATEST DAY: " + latest_refresh )
print("LATEST CLOSE: " + to_usd(float(latest_close)))
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

