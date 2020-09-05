# This script works on 2 columns in the tweets file received through the Twitter API: " screen_name" and " text" (note the blankspaces inserted by Twitter)
# To make it work with the output of GetOldTweets3, change the label username to screenname with a leading blankspace, and add a leading blankspace to the label text
# Line 94 has the input file name tweets.csv (change it as needed)
# Output file network_edges.csv has two columns.
# The first (left) column is the target and the second (right) column is the source in a directed network
import pandas as pd
import numpy as np
import os

#Definition for strippping whitespace
def trim(dataset):
    trim = lambda x: x.strip() if type(x) is str else x
    return dataset.applymap(trim)

def construct_edges(tweeters):
    """
    :param tweeters: a datafrmae of twitter handles
    :return: A dataframe of edges with 'handles of retweeted and reply/mentions' as first column
    and the twitter of handle of the tweeted person as the second column.
    """
    network_edges = []
    for idx, row in tweeters.iterrows():
        for name in list(np.array(row.rt_name).flat):
            network_edges.append({'rt_name': row[' screen_name'], ' screen_name': name })
    network_edges = pd.DataFrame(network_edges)
    return network_edges


def get_rt_names(tweets):
    """
    :param tweets: tweets file with all the columns.
    :return: tweeters with two columns:
                1. ' screen_name': the twitter handle of the person who tweeted
                2. the twitter handle of orignal tweets and any other mentions as a list.
    """
    import re

    def get_names(tweet):
        """
        Regular expression logic --- '^@.*': '^' - looks for the string starting with '@'
                                          '.' - any character
                                          '*' - repeating zero or more times
                                          Thus it looks for all the strings starting with '@'
                                 --- '[^\w]': '[]' : represents a character class
                                               '\w' : all alpha numeric characters including underscores
                                               '^': when used inside the character class it is a negation
                                        Thus it looks for all the non alpha numeric characters in a string.
        :param tweet: a row in the data frame of tweets.
        :return: a list of screen names mentioned in the tweet-text.
        """
        pattern = re.compile('^@.*')
        text = tweet[' text']
        text_tokens = str(text).split()
        screen_name = tweet[' screen_name']
        matches = []
        for tok in text_tokens:
            match_name = pattern.match(tok)
            if (match_name):
                rt_name = match_name.group()
                rt_name = re.sub('[^\w]', "", rt_name)
                matches.append(rt_name)
        if not matches:
            matches.append(screen_name)
        return matches

    if ' screen_name' in tweets.columns:
        if ' text' in tweets.columns:
            tweets['rt_name'] = tweets.apply(get_names, axis=1)
        else:
            print("please check for the column names")
            print(" 'text': column name for the tweet text is missing")
            print(" you might check for extra white spaces as well")
    else:
        print("please check for the column names")
        print(" ' screen_name': column name for the twitter profle name is missing")
        print(" you might check for extra white spaces as well")
    tweeters = tweets[[ 'rt_name', ' screen_name']]
    return tweeters


def read_csv():
    """
    :return: tweets file in latin1 encoding.
    """
    try:
        tweets = pd.read_csv('tweets.csv', encoding='latin1')

    except:
        print("File not found")
        print("Please check if the file named 'tweets.csv' exists in the directory:")
        print(os.getcwd() + "/")
        exit()
    return tweets


def main():
    """
    :tweeters: two column file with screen name of tweet and list of retweet names for each tweet
    :network_edges: created by taking tweeters and turning it into edgelist
    :network_edges.to_csv: outputs dataframe to file
    """
    from datetime import datetime
    tweets = read_csv()
    if tweets is None:
        return
    screen_name_list = []
    rt_name_list = []
    tweeters = get_rt_names(tweets)
    for row in range(0,len(tweeters[' screen_name'])):
        screen_name = tweeters[' screen_name'][row]
        for retweet in tweeters['rt_name'][row]:
            screen_name_list.append(screen_name)
            rt_name_list.append(retweet)     
    network_edges = pd.DataFrame()
    network_edges['rt_name'] = rt_name_list
    network_edges['screen_name'] = screen_name_list
    # file_name = str(os.getcwd()) + "\\" + "network_edges" + "_" + str(datetime.now()) + ".csv"
    network_edges.to_csv("output.csv", index=False)
    print("edges file is ready @: " + str(os.getcwd()))

# compile the file and run the function below.
main()
