# app/robo_advisor.py

#import certain modules/ packages
import requests
import json 
import os
import csv 

from datetime import datetime

from dotenv import load_dotenv
from environs import Env

load_dotenv()

#alpha_advantage specific 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

#defining key variables
now = datetime.now()
decision = ""

#defining applicable functions for main program
#to_usd function adapted from that one given/ developed by Professor Rossetti
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


# Your key here
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")




#receiving client inputs
print("")
print("Welcome to the FinServ 2.0 Robo Stock Advisor, where quality advice is offered for free!")
print("")
print("To use this program, input a stock ticker of your choice and receive a recommendation based on our proprietary algorithms")
print("")
symbol = input(print("Please input a stock ticker for a stock you which to get advice on: "))


#scrapping what is required from web 
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"

response = requests.get(request_url)

#some quick checks
#print(response.status_code) #> 200
#print(response.text)

#parse from the response text into dictionary
parsed_response = json.loads(response.text)

#handle response errors
if "Error Message" in response.text:
    print("OOPS, couldn't find that symbol, please try again and input symbols in the following format: MSFT")
    print("Please try run the program again. Thank you!")
    exit()


#print(parsed_response)
latest_refresh = parsed_response["Meta Data"]["3. Last Refreshed"]


#establishing output variables
time_series_keys = list(parsed_response["Time Series (Daily)"].keys())
latest_day_applicable = time_series_keys[0] 
latest_close = parsed_response["Time Series (Daily)"][latest_day_applicable]["4. close"]
latest_volume = parsed_response["Time Series (Daily)"][latest_day_applicable]["5. volume"]




#writing the data to a file
#define file name
file_name = f"prices_{symbol}.csv" 
csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", file_name)

#define column names
column_names= ["Timestamp", "Open", "High", "Low", "Close", "Volume"]
#define counters
total_volume = 0
total_close = 0.0
movement = 0.0;

#write in the items to the file
with open(csv_filepath, "w") as file:
    writer = csv.DictWriter(file, column_names)
    #write in the headers
    writer.writeheader()
    for date in time_series_keys:
        #loop each different timestamp row using this established row format 
        writer.writerow({
            "Timestamp": date,
            "Open": parsed_response["Time Series (Daily)"][date]["1. open"],
            "High": parsed_response["Time Series (Daily)"][date]["2. high"],
            "Low": parsed_response["Time Series (Daily)"][date]["3. low"],
            "Close": parsed_response["Time Series (Daily)"][date]["4. close"],
            "Volume": parsed_response["Time Series (Daily)"][date]["5. volume"],
        })

        #use some counters to get averages later
        total_volume += int(parsed_response["Time Series (Daily)"][date]["5. volume"])
        total_close += float(parsed_response["Time Series (Daily)"][date]["4. close"])


file.close()




#recent high/ low calculations
#define local variables
max = 0.0
min = 1000.0
y = 0
x = 0
#use while loop to calc. max and min
while (x <= 100 and y < len(time_series_keys)):
    high = float(parsed_response["Time Series (Daily)"][time_series_keys[y]]["2. high"])
    low = float(parsed_response["Time Series (Daily)"][time_series_keys[y]]["3. low"])
    if max < high:
        max = high
    elif min > low:
        min = low
    else:
        y +=1
        x +=1


 

#the famous proprietary algorithm ;)

#calculate averages to use for algorithm
average_volume = total_volume/(len(time_series_keys))
average_price = total_close/(len(time_series_keys))
adjusted_low_average = 0.4 * average_price
adjusted_low_volume = 0.2 * average_volume

#establishing an algocounter 
algo_counter = 0
#algorithm calculations
if float(latest_close) < adjusted_low_average:
    algo_counter += 1
if int(latest_volume) < adjusted_low_volume:
    algo_counter += 1


#the final and most crucial if
if algo_counter >= 5:
    decision = 'Buy'
elif algo_counter >=3:
    decision = "Neutral Weighting"
else:
    decision = "Sell"



#Program outputs
print("-------------------------")
print("SELECTED SYMBOL: " + symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print("LATEST DAY: " + latest_refresh )
print("LATEST CLOSE: " + to_usd(float(latest_close)))
print("RECENT HIGH: " + to_usd(max))
print("RECENT LOW: "+ to_usd(min))
print("-------------------------")
print("RECOMMENDATION: " + decision)
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
print("")
print("")


#data visualization
#this was adopted from the alpha vantage customer service website/ github
#https://medium.com/alpha-vantage/get-started-with-alpha-vantage-data-619a70c7f33a

key = ALPHA_VANTAGE_API_KEY
ts = TimeSeries(key, output_format='pandas')
ti = TechIndicators(key)

# Get the data, returns a tuple
# aapl_data is a pandas dataframe, aapl_meta_data is a dict
stock_data, stock_meta_data = ts.get_daily(symbol=symbol)
# aapl_sma is a dict, aapl_meta_sma also a dict
stock_sma, stock_meta_sma = ti.get_sma(symbol=symbol)

# Visualization
figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
stock_data['4. close'].plot()
plt.tight_layout()
plt.grid()
plt.show()


#sending an email part
#the code below is taken from prof. Rossetti's format for emailing content - this has been slightly adjusted to fit the
#variables and parameters of this code
#NOTE: this is mostly his code

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


#get customer email
print("")
CUST_ADDRESS = input("Input your email to receieve alerts for price movement news on your selected stock: ")
print("")
print("")
print("")

#calc movement 
movement = (float(latest_close) - (average_price) )/ average_price
movement_str = f"{0:,.2f}%".format(movement)

#only send the email if the price movement is significant 
if movement > 0.1 or movement < (-.1):
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID")
    MY_ADDRESS = os.environ.get("EMAIL")
    SUBJECT = 'Stock Price Movement Alert'


    client = SendGridAPIClient(SENDGRID_API_KEY)
    print("CLIENT:", type(client))

    message = Mail(from_email=MY_ADDRESS, to_emails=CUST_ADDRESS, subject=SUBJECT)
    print("MESSAGE:", type(message))

    message.template_id = SENDGRID_TEMPLATE_ID


    message.dynamic_template_data = {
        "symbol": symbol,
        "human_friendly_timestamp": now.strftime("%d-%m-%Y %I:%M %p"),
        "movement": movement_str
        }# or construct this dictionary dynamically based on the results of some other process :-D

    try:
        response = client.send(message)
        print("RESPONSE:", type(response))
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print("OOPS", e)


