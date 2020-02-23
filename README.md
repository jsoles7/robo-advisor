## The Project
A roject aiming to build a tool to automate the process of providing your clients with stock trading recommendations. This read me will help in guiding you to build out a basic sotck robo-advisor!


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

Fork the repo and clone it to your desktop. <br />
Navigate to the file from the commandline: <br />
- cd shopping-cart/ <br />

## Setting up the Environment:
conda create -n shopping-env python=3.7 # (first time only) <br />
conda activate shopping-env <br />
<br />

Proceed to download the following packages <br />
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

Make sure to configure your env to fit the required variables: <br />
- Sendgrid API KEY <br />
- Sendgrid API TEMPLATE <br />
- An email address to use for sending and receiving emailed recepits <br />
- Local tax rate <br />


## Usage:
Run the recommendation script: <br />
- python robo-advisor.py  <br />

## User Instructions:
The command line will ask the user to input a stock ticker <br />
Then, the program will run requests from Alpha Advantage in order to get the necessary stock information from real time date. It will obtain the information and transport it into the script, while simultaneously saving it into a CSV file. The program will output the data in a standardized format, displaying key numbers such as latest close, time accessed, highs and lows etc. <br />
Following this, the program will output a recommendation to either buy, sell, or hold on the basis of the results of a proprietary algorithm. Feel free to edit this algorithm to add any specificieties you like to include when thinking about picking a stock! <br />
Then, the program will ask the user for his or her email (he or she can decline if he or she wants to) and proceed to send them a price movement alert if the price moved drastically from its recent trading average. <br />





