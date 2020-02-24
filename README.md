## The Project
A project aiming to build a tool to automate the process of providing your clients with stock trading recommendations. This read me will help in guiding you to build out a basic sotck robo-advisor!


## Prerequisites:
- Anaconda 3.7 <br />
- Python 3.7 <br />
- Pip

## Required Python Packages & Modules:
- datetime <br />
- dotenv <br />
- os <br />
- pandas <br />
- sendgrid <br />
- environms <br />
- CSV <br />
- alpha_vantage.timeseries <br />
- alpha_vantage.techindicators <br />
- matplotlib.pyplot <br />


## Installation:
In order to set this project up, please download this repo and write into the command line: <br />
    - git clone git@github.com:jsoles7/robo-advisor-py <br />
    - cd robo-advisor-py/ <br />

Proceed to download the following packages: <br />
- pip install python-dotenv <br />
- pip install sendgrid==6.0.5 <br />
- pip install pandas <br />
- pip install environs <br />
- pip install requests <br />
- pip install matplotlib <br />
- pip install alpha_vantage <br />

<br />
**Note that you can simply run the command 'pip install -r requirements.txt' to expedite the above process
<br />

## Setting up the Environment:
conda create -n robo-advisor-env python=3.7 # (first time only) <br />
conda activate robo-advisor-env <br />
<br />

## Set Up
Before setting up the basics of the project, make sure to obtain an Alpha Vantage API key at: https://www.alphavantage.co/support/#api-key <br />
After obtaining the key, make sure to copy this key and place it into your .env file (Don't worry, the ".env" has already been ignored from version control) <br />
Proceed to naviagte the commandline to the appropriate directory that contains the project. <br />

In addition to what was said above, make sure to configure your env to fit the required variables: <br />
- Sendgrid API KEY <br />
- Sendgrid API TEMPLATE <br />
- An email address to use for sending and receiving emailed alerts <br />

For information on how to obtain a Sendgrid API key and tempate (it's very easy by the way so don't be too concerned), check out these two explanatory links: <br />
- https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/sendgrid.md
- https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/sendgrid.md#email-templates
- https://github.com/prof-rossetti/intro-to-python/blob/master/exercises/emails-with-templates/send_email.py


## Usage:
Run the recommendation script: <br />
- python app/robo-advisor.py  <br />

## User Instructions:
The command line will ask the user to input as many stock tickers as you like. Note that in order to stop inputting stock tickers, you need to write in 'DONE'. <br />
Moreover, it will ask the user if he or she would like to enter his or her email to send stock alerts. In the case that the user says yes, the email will be saved and used later on. <br />

Then, the program will run on a per-stock basis (done via using a for loop). The procedure runs as follows:
- Obtain requests from Alpha Advantage in order to get the necessary stock information from real time date. It will obtain the information and transport it into the script, while simultaneously saving it into a CSV file. 
- Calculate certain key and required values, in order to output later. <br /> 
- Formulate a recommendation based on an algorithm that recommends either to buy, sell, or hold on the basis of some simple formulas. Feel free to edit this algorithm to add any specificieties you like to include when thinking about picking a stock! The recommendation algorithm I used was based on a couple of theories of technical analysis/ paired with a basic idea of value investing. <br />
- The program will output the data in a standardized format, displaying key numbers such as latest close, time accessed, highs and lows etc. <br />
- Following this, the program will output the recommendation and a standardized reasoning for it, explaining the theory behind the recommendation in a human-friendly way. <br />
- Then, depending on whether the user said yes to receiving alert emails, the program proceed to send them a price movement alert if the price moved drastically from its recent trading average. <br />
- The program then concludes with a warm message, while also asking for feedback. <br />


DISCLAIMER: the authors of this program bear no liability for gains/losses on investments made based on the outputed recommendations.


