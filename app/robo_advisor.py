# app/robo_advisor.py

#import certain modules/ packages
import requests
import json 
from datetime import datetime

#defining key variables
now = datetime.now()

#scrapping what is required from web 
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo "

response = requests.get(request_url)

print(response.status_code) #> 200
#print(response.text)

#parse from the response text into dictionary
parsed_response = json.loads(response.text)
#print(parsed_response)
latest_refresh = parsed_response["Meta Data"]["3. Last Refreshed"]

#receiving client inputs
 


#Program outputs
print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print("LATEST DAY: " + latest_refresh )
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

