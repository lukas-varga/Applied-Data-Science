#!/usr/bin/env python
# coding: utf-8

# # OTH - Twitter Data Analysis
# ## Lukáš Varga

# ### 1.1 Credentials

# In[ ]:


import json

#my credentials
credentials = {}
credentials["CONSUMER_KEY"] = ""
credentials["CONSUMER_SECRET"] = ""
credentials["BEARER_TOKEN"] = ""
credentials["ACCESS_TOKEN"] = ""
credentials["ACCESS_TOKEN_SECRET"] = ""

#save to json
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)
    
print("JSON file with credentials was created!")
print("Done!")


# ### 1.2 Initialize

# In[ ]:


#imports
import json #JSON credentials
import csv #CSV results
import tweepy as tw #twitter API
import pandas as pd #dataframes
from textblob import TextBlob #sentiment
import re #regex
import matplotlib.pyplot as plt #graphs
import sys #max integer

#asking user about event
EVENT = input("Please enter the event: #")
EVENT = EVENT.lower()
SEARCH_EVENT = "#" + str(EVENT) + "-filter:retweets"

#parameters for filtering
#SINCE_DATE = "2021-01-01"
#ITEM_NUM = 100
SINCE_DATE = input("Enter the oldest possible date of tweets. Use format \"YYYY-MM-DD\": ")
ITEM_NUM_STR = input("Enter the maximum number of tweets (Empty for no limit): ")

ITEM_NUM = sys.maxsize
if(len(ITEM_NUM_STR) != 0):
    ITEM_NUM = int(ITEM_NUM_STR)
print("Loading data set...")

#load credentials
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

#set authentification
auth = tw.OAuthHandler(creds["CONSUMER_KEY"], creds["CONSUMER_SECRET"])
auth.set_access_token(creds["ACCESS_TOKEN"], creds["ACCESS_TOKEN_SECRET"])
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#get data set

tweets = tw.Cursor(api.search,
                   q = SEARCH_EVENT,
                   lang = "en",
                   since = SINCE_DATE).items(ITEM_NUM)

tweets_dataset=[]
for tweet in tweets:
    hashtags = tweet.entities.get("hashtags")
    tags=[]
    for hashtag in hashtags:
        tag = hashtag['text'].lower()
        tags.append(tag)
    tweets_dataset.append([tweet.author.screen_name,tweet.author.name,tweet.text,tags])
    
df_tweets = pd.DataFrame(tweets_dataset,columns=["user","real_name","text","hashtags"])

size = len(df_tweets.index)
#pd.set_option("display.max_rows",size)
pd.reset_option("display.max_rows")
display(df_tweets)

print("Data set has been loaded!")
print("Done!")


# ### 2.1 Derive the sentiment

# In[ ]:


#SENTIMENT
print("Computing sentiment...")

#delete all URLs and unallowed chars using REGEX
def remove_url(text):
    return " ".join(re.sub("(\w+:\/\/\w+)|([^0-9A-Za-z\t ])", "", text).split())

texts = df_tweets["text"]
clear_tweets = []
for text in texts:
    clear_tweets.append(remove_url(text))

#creting obj using TextBlob
sentim_obj = []
for text in clear_tweets:
    sentim_obj.append(TextBlob(text))

#extracting polarity  
sentim_values = []
for tweet in sentim_obj:
    sentim_values.append([str(tweet),tweet.sentiment.polarity])

#creating dataframe with results
sentiment_df = pd.DataFrame(sentim_values, columns=["clear_tweet","sentiment"])

#histogram (w/o zero values for better visualisation)
clear_sentiment_df = sentiment_df[sentiment_df.sentiment!=0]
x=clear_sentiment_df["sentiment"]

fig, ax = plt.subplots()
ax.set_xlabel("Sentiment (Omitting 0 values)")
ax.set_ylabel("Counts")
ax.set_title("Histogram of sentiments in #"+EVENT)
ax.hist(x,bins=[-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
plt.grid(True)

#display and save histogram
plt.savefig("01_sentiment_vis.png")
print("PNG file of sentiments was created!")
plt.show()


#display and save dataframe
sentiment_df.to_csv("01_sentiment_res.csv",index=False,sep=";")
print("CSV file of sentiments was created!")

size = len(sentiment_df.index)
pd.set_option("display.max_rows",size)
#pd.reset_option("display.max_rows")
display(sentiment_df)

print("Done!")


# ### 2.2 Top 10 hashtags and users 

# In[ ]:


#TOP10 hashtags
print("Looking for Top 10 hashtags...")

hashtags_dict={}

for i in range(len(df_tweets)):
    hashtahgs = df_tweets.loc[i,"hashtags"]
    for tag in hashtahgs:
        if tag in hashtags_dict.keys():
            hashtags_dict[tag] += 1
        else:
            hashtags_dict[tag] = 1

sorted_hashtags_dict = sorted(hashtags_dict, key=hashtags_dict.get, reverse=True)
top_hashtags_dict={}
i=0

for hashtag in sorted_hashtags_dict:
    if(i==10):
        break
    top_hashtags_dict[hashtag] = hashtags_dict[hashtag]
    i+=1

    
res_hashtags = []
for hashtag in top_hashtags_dict:
    res_hashtags.append([hashtag,top_hashtags_dict[hashtag]])
    
df_hashtags = pd.DataFrame(res_hashtags, columns=["#hashtag","occurrence"])
df_hashtags.to_csv('02_top10_hashtags.csv',index=False,sep=";")
print("CSV file of Top 10 hashtags was created!")

size = len(df_hashtags.index)
pd.set_option("display.max_rows",size)
#pd.reset_option("display.max_rows")
display(df_hashtags)


#TOP10 users
print("Looking for Top 10 users...")

users_dict={} #user->counts
names_dict={} #user->name
users = []

for i in range(len(df_tweets)):
    user = df_tweets.loc[i,"user"]# @user
    name = df_tweets.loc[i,"real_name"]# alias
    if user in users_dict.keys():
        users_dict[user] += 1
    else:
        users_dict[user] = 1
        names_dict[user] = name
     
    
sorted_users_dict = sorted(users_dict, key=users_dict.get, reverse=True)
top_users_dict={}
top_names_dict={}
i=0

for user in sorted_users_dict:
    if(i==10):
        break
    top_users_dict[user] = users_dict[user]
    top_names_dict[user] = names_dict[user]
    i+=1

res_users = []
for user in top_users_dict:
    res_users.append([user,top_names_dict[user],top_users_dict[user]])
    
df_users = pd.DataFrame(res_users, columns=["@user","real_name","occurrence"])

df_users.to_csv('02_top10_users.csv',index=False,sep=";")
print("CSV file of Top 10 users was created!")

size = len(df_users.index)
pd.set_option("display.max_rows",size)
#pd.reset_option("display.max_rows")
display(df_users)


print("Done!")


# ### 2.3 Followers of a given user

# In[ ]:


#FOLLOWERS
print("Displaying usernames in data set...")

#displaying users to choose
users=[]
for i in range(len(df_tweets)):
    users.append(df_tweets.loc[i,"user"])
    
df_users = pd.DataFrame(users, columns=["dataset_@user"])
df_users.drop_duplicates(subset=["dataset_@user"], keep="first", inplace=True)
df_users = df_users.reset_index(drop=True)
    
size = len(df_users.index)
pd.set_option("display.max_rows",size)
#pd.reset_option("display.max_rows")
display(df_users)

USER_NAME = input("Please provide a username to examine his followers: ")
USER_COUNT_STR = input("Please provide a max number of results (Empty for no limit): ")

USER_COUNT = sys.maxsize
if(len(USER_COUNT_STR) != 0):
    USER_COUNT = int(USER_COUNT_STR)
print("Looking for followers...")

users = tw.Cursor(api.followers,
                  screen_name = USER_NAME).items(USER_COUNT)

followers = []
for user in users:
    followers.append([user.screen_name, user.name])

df_followers = pd.DataFrame(followers, columns=["@user","real_name"])

df_followers.to_csv('03_followers.csv',index=False,sep=";")
csv = f"CSV file of followers of the user @{USER_NAME} was created!"
print(csv)
    
size = len(df_followers.index)
pd.set_option("display.max_rows",size)
display(df_followers)

print("Done!")


# ### 2.4 Tweets and profiles of all followers 

# In[ ]:


#TWEETS
print("Displaying usernames in data set...")

#displaying users to choose
users=[]
for i in range(len(df_tweets)):
    users.append(df_tweets.loc[i,"user"])
    
df_users = pd.DataFrame(users, columns=["dataset_@user"])
df_users.drop_duplicates(subset=["dataset_@user"], keep="first", inplace=True)
df_users = df_users.reset_index(drop=True)
    
size = len(df_users.index)
pd.set_option("display.max_rows",size)
#pd.reset_option("display.max_rows",size)
display(df_users)

USER_NAME = input("Please provide a username to get his tweets and profiles of followers: ")

TWEET_COUNT_STR = input("Please provide a max number of tweets (Empty for no limit): ")
TWEET_COUNT = sys.maxsize
if(len(TWEET_COUNT_STR) != 0):
    TWEET_COUNT = int(TWEET_COUNT_STR)
    
PROFILE_COUNT_STR = input("Please provide a max number of profiles (Empty for no limit): ")
PROFILE_COUNT = sys.maxsize
if(len(PROFILE_COUNT_STR) != 0):
    PROFILE_COUNT = int(PROFILE_COUNT_STR)


print("Looking for tweets of given user...")
    
tweets = tw.Cursor(api.user_timeline,
                  id = USER_NAME).items(TWEET_COUNT)

tweets_arr = []
for tweet in tweets:
    tweets_arr.append(tweet.text)

df_texts = pd.DataFrame(tweets_arr, columns=["text"])

df_texts.to_csv('04_tweets.csv',index=False,sep=";")
csv = f"CSV file of tweets of the user @{USER_NAME} was created!"
print(csv)
    
size = len(df_texts.index)
pd.set_option("display.max_rows",size)
#pd.reset_option("display.max_rows")
display(df_texts)

print("Done!")

#PROFILES
print("Looking for profiles of given user...")
    
users = tw.Cursor(api.followers,
                  screen_name = USER_NAME).items(PROFILE_COUNT)

profiles_arr = []
for user in users:
    profile = f"https://twitter.com/{user.screen_name}"
    profiles_arr.append([user.screen_name, user.name, profile])

df_profiles = pd.DataFrame(profiles_arr, columns=["user","real_name","profile"])

df_profiles.to_csv('04_profiles.csv',index=False,sep=";")
csv = f"CSV file of profiles of the user @{USER_NAME} was created!"
print(csv)
    
size = len(df_profiles.index)
pd.set_option("display.max_rows",size)
#pd.reset_option("display_max_rows")
display(df_profiles)

print("Done!")


# In[ ]:




