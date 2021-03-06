# app/robo_advisor.py

#import certain modules/ packages
import requests
import json 
import os
import csv 
import matplotlib.pyplot as plt



#defining applicable functions for main program (avoiding code reduplication)
#to_usd function adapted from that one given/ developed by Professor Rossetti
def to_usd(my_price):
    """
        This function is used to convert float numbers passed to it to a formatted price in traditional US format.

        Source: Prof. Rossetti's In class Example.

        @param: the my_price variable is a price input that comes as a float (e.g. 13.98570) and 
                represents a variable that is supposed to be converted to a price format.

    """
    return "${0:,.2f}".format(my_price)

#error message printing function
def print_input_err_message():
    """
        This function prints an error message and then exits. It occurs whenever there is input validation errors or HTTP request errors.

        @param: none.

    """

    print("")
    print("OOPS, couldn't find that symbol, please try again and input symbols in the following format: MSFT")
    print("Please try run the program again. Thank you!")
    print("")
    exit()

#max/ min calc functions
def min_calc(total_days, dictionary, time_series):
    """
        This function is used to calculate the minimum share price given a set of days. 
        It proceeds to tally up the lows for each of those days in the given range.
        It will then get the minimum out of those lows to calculate a share price.

        @param: three inputs are required for this function: the first is an integer that represents total days for which
                you wish to calculate the minimum (e.g. 100); the second is a dictionary that is passed; and the 
                third is a list that is supposed to contain the different day keys.

    """

    #define local variables
    min_1 = 10000.0
    t = 0
    #use while loop to calc. max and min
    while (t < total_days):
        low = float(dictionary["Time Series (Daily)"][time_series[t]]["3. low"])
        if min_1 > low:
            min_1 = low
        t +=1
    return min_1 

def max_calc(total_days, dictionary, time_series):
    """
        This function is used to calculate the maximum share price given a set of days. 
        It proceeds to tally up the highs for each of those days in the given range.
        It will then get the maximum out of those lows to calculate a share price.

        @param: three inputs are required for this function: the first is an integer that represents total days for which
                you wish to calculate the maximum (e.g. 100); the second is a dictionary that is passed; and the 
                third is a list that is supposed to contain the different day keys.

    """
    #define local variables
    max_1 = 0
    t = 0
    #use while loop to calc. max and min
    while (t < total_days):
        high = float(dictionary["Time Series (Daily)"][time_series[t]]["2. high"])
        if max_1 < high:
            max_1 = high
        t +=1
    return max_1 

def algo_output(algo_counter):
    """
        This function is used to determine the appropriate output for the algorithm.
        It takes in the algo_counter number as an argument (determined by calculations in the script),
        And it spits out the recommended action and reason.

        @param: algo_counter is a numeric input that comes as an integer and represents the score the algorithm's calculations
                have have given so far.

    """
    if algo_counter == 2:
        reason = "BUY: Due to the numerous functions and analyses the program run, the stock was identified as having the potential to be undervalued. "
        reason = reason + "FinServ's algorithm looked at the stock's relation to trading patterns and identified it as being in a dip. "
        reason = reason + "With this as the case, there is a stronger chance of regression to the mean, implying some upside to be made! "
        reason = reason + "Feel free to check out more on this theory of investing @ https://www.investopedia.com/articles/active-trading/102914/technical-analysis-strategies-beginners.asp"
    elif algo_counter == 1:
        reason = "NEUTRAL WEIGHTING: Due to the numerous functions and analyses the program run, the stock was identified as having the potential to be neither overvalued or undervalued. "
        reason = reason + "FinServ's algorithm looked at the stock's relation to trading patterns and identified it as being inline with current performance. "
        reason = reason + "With this as the case, there is a minimal chance of regression to the mean, implying some no upside or downside. "
        reason = reason + "Feel free to check out more on this theory of investing @ https://www.investopedia.com/articles/active-trading/102914/technical-analysis-strategies-beginners.asp"
    else:
        reason = "SELL: Due to the numerous functions and analyses the program run, the stock was identified as having the potential to be overvalued. "
        reason = reason + "FinServ's algorithm looked at the stock's relation to trading patterns and identified it as being at a crest. "
        reason = reason + "With this as the case, there is a stronger chance of regression to the mean, implying some downside to potentially be met. "
        reason = reason + "Feel free to check out more on this theory of investing @ https://www.investopedia.com/articles/active-trading/102914/technical-analysis-strategies-beginners.asp"

    return reason

def input_validation(input):
    """
        This function is used to test the stock ticker inputs and validate that they
        pass the two key characteristics tests: being less than 5 characters in length
        and having no digits.

        @param: input is a string argument that represents the given input the consumer gave as a ticker.

    """
    result_bool = True 

    if any(char.isdigit() for char in input) == True:
        result_bool = False

    if len(input) > 5:
        result_bool = False
    
    return result_bool

def request_url(ticker, API_key):
    """
        This function is used to compile an accessible ALPHA VANTAGE link using he ticker and API key as inputs.
        This allows the program to use the API to get stock data.

        @param: two parameters are passed to this function. The first is the ticker (which has already been validated) 
                and is a string. The second is the API key which is a string.

    """
    link = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol={ticker}&apikey={API_key}"
    return link 

def adj_low_price(mean_price):
    """
        This function is used to calculate an adjusted mean value in order to use it in the algorithm calculations.
        It takes 40% of the average given.

        @param: the parameter is a float variable that is supposed to be the mean price calculated from the time_series data.

    """
    return 0.4 * mean_price

def adj_low_volume(mean_volume):
    """
        This function is used to calculate an adjusted mean value in order to use it in the algorithm calculations.
        It takes 20% of the average given.

        @param: the parameter is a float variable that is supposed to be the mean volume calculated from the time_series data.

    """
    return 0.2 * mean_volume

def visualization(key, s):
    """
        This function is used to create the stock chart visualization. It receives the API key and the ticker
        as arguments and then produces the plot as a result.

        @param: this function has two parameters: the first is the API key that is a string. The second is the stock ticker
                which is a string and has already been validated. 

    """
    #this was adopted from the alpha vantage customer service website/ github
    #https://medium.com/alpha-vantage/get-started-with-alpha-vantage-data-619a70c7f33a
    key = ALPHA_VANTAGE_API_KEY
    ts = TimeSeries(key, output_format='pandas')
    ti = TechIndicators(key)

    # Get the data, returns a tuple
    # stock_data is a pandas dataframe
    # note that the API is requested one more time 
    stock_data, stock_meta_data = ts.get_daily(symbol=s)


    # Visualization
    figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
    stock_data['4. close'].plot()
    plt.tight_layout()
    plt.grid()
    plt.show()

def movement_calc(latest_price, average):
    """
        This function is used to calculate a movement variable used to determine email content.
        It takes in a latest price and an average price and determines the percent change.

        @param: this function has two parameters: the first is a float variable that is the latest price calculated
                from the time_series. The second is the average price, a float variable, calculated from the time_series. 
    """
    numerator = latest_price - average
    answer = numerator/ average
    return answer


#main program

if __name__ == "__main__":

    from datetime import datetime

    from dotenv import load_dotenv
    from environs import Env

    load_dotenv()

    #alpha_advantage specific 
    from alpha_vantage.timeseries import TimeSeries
    from alpha_vantage.techindicators import TechIndicators
    from matplotlib.pyplot import figure


    #defining key variables
    now = datetime.now()

    # Key here
    ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")


    #PART 1: client inputs and program initialization

    #receiving client inputs
    print("")
    print("Welcome to the FinServ 2.0 Robo Stock Advisor, where quality advice is offered for free!")
    print("")
    print("To use this program, input a stock ticker of your choice and receive a recommendation based on our proprietary algorithms")
    print("")

    #define list + symbol
    symbols_list = []
    symbol = ""

    #input multiple stocks:
    while symbol != "DONE":
        symbol = input(print("Please input a stock ticker for a stock you which to get advice on. When you are done entering tickers (MAXIMUM of two stocks), please type DONE: "))
        symbol = symbol.upper()
        #some quick prelimenary input validation (in order to save time of issuing a get request)
        check = input_validation(symbol)
        if check == True:
            symbols_list.append(symbol)
        else:
            print_input_err_message()
        

    #first verify if customer wants to get an email (important for UX)
    customer_response_email = input("Before we begin, would you like to enter your email in order to receive price movement alerts? (Enter 'YES' if so) ")
    customer_response_email = customer_response_email.upper()

    if customer_response_email == "YES":
        #ask for email 
            print("")
            CUST_ADDRESS = input("Input your email to receieve alerts for price movement news on your selected stock: ")
            print("")
            print("")
            print("")
    #will be used later to judge when sending emails

    #remove the DONE
    symbols_list.pop()


    #PART 2: taking in the tickers and obtaining the data from the server online + running important calculations on the data

    #running loop to run analysis for each symbol 
    for s in symbols_list:

        #proceed to scrape, one additional input check is provided below to catch any other errors 
        #scrapping what is required from web 
        url = str(request_url(s, ALPHA_VANTAGE_API_KEY))

        response = requests.get(url)

        #parse from the response text into dictionary
        parsed_response = json.loads(response.text)

        #handle response errors
        if "Error Message" in response.text:
            print_input_err_message()
        elif "ValueError" in response.text:
            print_input_err_message()


        #print(parsed_response)
        latest_refresh = parsed_response["Meta Data"]["3. Last Refreshed"]

        #establishing output variables

        #running a while loop to collect the tradeable days info 
        time_series_keys = list(parsed_response["Time Series (Daily)"].keys())
        
        latest_day_applicable = time_series_keys[0] 
        latest_close = parsed_response["Time Series (Daily)"][latest_day_applicable]["4. close"]
        latest_volume = parsed_response["Time Series (Daily)"][latest_day_applicable]["5. volume"]

        #52-week high/ low calculations
        max_52 = max_calc(253,parsed_response,time_series_keys)
        min_52 = min_calc(253,parsed_response,time_series_keys)


        #PART 2.5: Writing the data into a CSV file

        #writing the data to a file
        #define file name
        file_name = f"prices_{s}.csv" 
        csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", file_name)

        #define column names
        column_names= ["Timestamp", "Open", "High", "Low", "Close", "Volume"]
        #define counters
        total_volume = 0
        total_close = 0.0
        movement = 0.0

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

        #close the file
        file.close()

        #END of file writing 



        #recent high/ low calculations
        #define local variables
        max_100 = max_calc(100,parsed_response,time_series_keys)
        min_100 = min_calc(100,parsed_response,time_series_keys)


        #PART 3: The Algorithm calculation 

        #calculate averages to use for algorithm
        average_volume = total_volume/(len(time_series_keys))
        average_price = total_close/(len(time_series_keys))
        adjusted_low_average = adj_low_price(average_price)
        adjusted_low_volume = adj_low_volume(average_volume)

        #establishing an algocounter 
        counter = 0
        #algorithm calculations
        if float(latest_close) < adjusted_low_average:
            counter += 1
        if int(latest_volume) < adjusted_low_volume:
            counter += 1


        #the final and most crucial if
        recommendation = algo_output(counter)


        #PART 4: The Program outputs (in a UX-friendly way)
        print("-------------------------")
        print("SELECTED SYMBOL: " + s)
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA...")
        print("REQUEST AT: " + now.strftime("%Y-%m-%d %I:%M %p"))
        print("-------------------------")
        print("LATEST DAY: " + latest_refresh )
        print("LATEST CLOSE: " + to_usd(float(latest_close)))
        print("RECENT HIGH: " + to_usd(max_100))
        print("RECENT LOW: "+ to_usd(min_100))
        print("-------------------------")
        print("52-WEEK HIGH: " + to_usd(max_52))
        print("52-WEEK LOW: "+ to_usd(min_52))
        print("-------------------------")
        print("RECOMMENDATION: " + recommendation)
        print("-------------------------")
        print("")
        print("")


        #Part 5: Data Visualization
        

        visualization(ALPHA_VANTAGE_API_KEY, s)
    

        #Part 6: Customer Email and SendGrid Integration

        #get customer email
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail


        #if customer wants to get an email, run the email-sending code 
        if customer_response_email == 'YES':

            #calc movement 
            movement = (movement_calc(latest_close, average_price))*100
            movement_str = f"{movement:,.2f}%"

            #only send the email if the price movement is significant 

            #sending an email part
            #the code below is taken from prof. Rossetti's format for emailing content - this has been slightly adjusted to fit the
            #variables and parameters of this code
            #NOTE: this is mostly his code

            if ( movement > 0.1 or movement < (-.1) ):
                #get variables from .env
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
                    "symbol": s,
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


    #Part 7: Conclusion of Program

    print("")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")
    print("")

    #concluding statement to thank the client for using the service
    print("")
    print("")
    print("Thank you for using FinServ 2.0 Robo Stock Advisor! We hope you got the information you were looking for \n")
    print("If you think there is a way we can improve our service, contact us at customerrelations@finserv.io")
    print("")