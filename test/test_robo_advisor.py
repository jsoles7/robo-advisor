

from app.robo_advisor import to_usd, algo_output, input_validation, request_url

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