Required libraries:
pip install tweepy
pip instal pandas
pip install textblob
pip install matplotlib

Required imports:
import json #JSON credentials
import csv #CSV results
import tweepy as tw #twitter API
import pandas as pd #dataframes
from textblob import TextBlob #sentiment
import re #regex
import matplotlib.pyplot as plt #graphs
import sys #max integer

Instructions:
User will execute commands in Jupyter Notebook (filename: twitter_varga.ipynb). Each scripts is ended with printing “Done!” so user knows once the computing is already finished. Sometimes when there is too much requests per time there might appear following disclaimer below to inform user that the program need to wait a certain amount of time in seconds to continue requesting Twitter API. It might appear when there is too large limit of results or when user repeatedly executing one command. It is not a bug, but the limitation of Twitter API.
	Rate limit reached. Sleeping for: #

The first thing user need to do is run script 1.1 Creentials, which creates a JSON file with keys and tokens to API. 

Then user proceed to script 1.2 Initialize. It loads all needed imports and create dataset base on user inputs below. We need to ask user about date and limit because the computation can take a long time when the rate limit is reached. Twitter has a policy of limiting higher number of requests per given time. 
	Please enter the event: #biden
	Enter the oldest possible date of tweets. Use format "YYYY-MM-DD": 2021-01-01
	Enter the maximum number of tweets (Empty for no limit): 500
 
The scripts 2.1 and 2.2 do not need any inputs. Therefore, after their execution they provide the results and also inform user about generated output files on disk.

In the script 2.3 user get a list of all users in data set and he is asked about choose one of them to privde him results. Again there is limitation due to rate limits.
	Please provide a username to examine his followers: KayCee_313
	Please provide a max number of results (Empty for no limit): 

The last script 2.4 similarly shows user a table with user to choose and then ask him about one and about limiting of number of results.
	Please provide a username to get his tweets and profiles of followers: KayCee_313
	Please provide a max number of tweets (Empty for no limit): 
	Please provide a max number of profiles (Empty for no limit): 