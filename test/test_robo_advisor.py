

from app.robo_advisor import to_usd, algo_output, input_validation, request_url, adj_low_volume, adj_low_price, movement_calc, min_calc, max_calc

def test_to_usd():
    #Should apply correct formatting
    assert to_usd(7.25) == "$7.25"

    #Should display two decimal places
    assert to_usd(8.5) == "$8.50"

    #Should round to two places
    assert to_usd(3.444444) == "$3.44"

    #Should display comma separators
    assert to_usd(1234567890.5555555) == "$1,234,567,890.56"

def test_algo_output():
    #Should result in a sell recommendation
    assert algo_output(0) == "SELL: Due to the numerous functions and analyses the program run, the stock was identified as having the potential to be overvalued. FinServ's algorithm looked at the stock's relation to trading patterns and identified it as being at a crest. With this as the case, there is a stronger chance of regression to the mean, implying some downside to potentially be met. Feel free to check out more on this theory of investing @ https://www.investopedia.com/articles/active-trading/102914/technical-analysis-strategies-beginners.asp"

    #Should result in a buy recommendation
    assert algo_output(2) == "BUY: Due to the numerous functions and analyses the program run, the stock was identified as having the potential to be undervalued. FinServ's algorithm looked at the stock's relation to trading patterns and identified it as being in a dip. With this as the case, there is a stronger chance of regression to the mean, implying some upside to be made! Feel free to check out more on this theory of investing @ https://www.investopedia.com/articles/active-trading/102914/technical-analysis-strategies-beginners.asp"

def test_input_validation():
    #Should result in False
    assert input_validation("45ab") == False

    #Should result in False
    assert input_validation("AAPLDEFJ") == False

    #Should result in True
    assert input_validation("TSLA") == True


def test_request_url():
    #Should return the correct link in proper format
    link = request_url("MSFT", "API_KEY")
    assert link == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=MSFT&apikey=API_KEY"

def test_adj_low_price():
    #Should return the 40% of the given number
    result = adj_low_price(100)
    assert result == 40


def test_adj_low_volume():
    #Should return the 20% of the given number
    vol = adj_low_volume(100)
    assert vol == 20

def test_movement_calc():
    #Should return the % change
    latest = 25 
    average = 20
    assert movement_calc(latest, average) == .25

def test_min_calc():
    response = {
    "Meta Data": {
        "1. Information": "Daily Time Series with Splits and Dividend Events",
        "2. Symbol": "IBM",
        "3. Last Refreshed": "2020-04-13",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2020-04-13": {
            "1. open": "121.6300",
            "2. high": "121.8000",
            "3. low": "118.0400",
            "4. close": "121.1500",
            "5. adjusted close": "121.1500",
            "6. volume": "5087275",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        },
        "2020-04-09": {
            "1. open": "120.4800",
            "2. high": "122.9200",
            "3. low": "120.1672",
            "4. close": "121.5000",
            "5. adjusted close": "121.5000",
            "6. volume": "5576210",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        },
        "2020-04-08": {
            "1. open": "116.3100",
            "2. high": "119.9600",
            "3. low": "115.0742",
            "4. close": "119.2900",
            "5. adjusted close": "119.2900",
            "6. volume": "5155987",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        },
        "2020-04-07": {
            "1. open": "118.8000",
            "2. high": "119.5700",
            "3. low": "114.8700",
            "4. close": "114.9400",
            "5. adjusted close": "114.9400",
            "6. volume": "5592463",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        },
        "2020-04-06": {
            "1. open": "110.3500",
            "2. high": "115.6300",
            "3. low": "110.1300",
            "4. close": "114.8200",
            "5. adjusted close": "114.8200",
            "6. volume": "7026457",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        }
        }
    }
    keys_list = ["2020-04-13","2020-04-09", "2020-04-08","2020-04-07","2020-04-06"]
    #Should return the minimum low
    assert min_calc(5, response, keys_list) == 110.1300


def test_max_calc():
    response = {
    "Meta Data": {
        "1. Information": "Daily Time Series with Splits and Dividend Events",
        "2. Symbol": "IBM",
        "3. Last Refreshed": "2020-04-13",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2020-04-13": {
            "1. open": "121.6300",
            "2. high": "121.8000",
            "3. low": "118.0400",
            "4. close": "121.1500",
            "5. adjusted close": "121.1500",
            "6. volume": "5087275",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        },
        "2020-04-09": {
            "1. open": "120.4800",
            "2. high": "122.9200",
            "3. low": "120.1672",
            "4. close": "121.5000",
            "5. adjusted close": "121.5000",
            "6. volume": "5576210",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        },
        "2020-04-08": {
            "1. open": "116.3100",
            "2. high": "119.9600",
            "3. low": "115.0742",
            "4. close": "119.2900",
            "5. adjusted close": "119.2900",
            "6. volume": "5155987",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        },
        "2020-04-07": {
            "1. open": "118.8000",
            "2. high": "119.5700",
            "3. low": "114.8700",
            "4. close": "114.9400",
            "5. adjusted close": "114.9400",
            "6. volume": "5592463",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        },
        "2020-04-06": {
            "1. open": "110.3500",
            "2. high": "115.6300",
            "3. low": "110.1300",
            "4. close": "114.8200",
            "5. adjusted close": "114.8200",
            "6. volume": "7026457",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0000"
        }
        }
    }
    keys_list = ["2020-04-13","2020-04-09", "2020-04-08","2020-04-07","2020-04-06"]
    #Should return the maximum high
    assert max_calc(5, response, keys_list) == 122.9200