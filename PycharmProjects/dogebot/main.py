from config import *
import requests
import pandas as pd
import numpy as np
import os
import json

#select a user#
def create_url():
    '''
    Select which username to get user id for. You can enter up to 100 comma separated values.

    :return: url as str
    '''
    usernames = "usernames=elonmusk"
    user_fields = "user.fields=description,created_at"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url

def create_headers(bearer_token):
    '''
    :param bearer_token: str; you get this from the Twitter API developer portal
    :return: dict
    '''

    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers, params):
    '''
    Connect to Twitter API endpoint using user URL and bearer token.

    :param url: str, from create_url()
    :param headers: dict, from create_headers()
    :param params: dict
    :return: dict (json object)
    '''

    ids_lookup = requests.request("GET", url, headers=headers)
    tweet_lookup = requests.response('GET', url, params=params)
    if ids_lookup.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                ids_lookup.status_code, ids_lookup.text
            )
        )

    if tweet_lookup.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                tweet_lookup.status_code, tweet_lookup.text
            )
        )
    return ids_lookup.json(), tweet_lookup.json()

def get_userid():
    '''
    Get userids for users entered in create_urls() function

    :return: list of strings
    '''

    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers, params)
    user_ids = [user['id'] for user in json_response['data']]
    #print(user_ids)
    return user_ids

get_userid()

#get all Elon's tweets between two dates
def get_tweets(date_from, date_to):
    '''
    Get tweets from a particular user using their user id

    :param date_from: utc-date
    :param date_to: utc-date
    :return: list of strings
    '''

    user_ids = get_userid()


