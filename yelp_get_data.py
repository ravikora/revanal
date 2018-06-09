#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 15:51:41 2018

@author: ravi
"""
import http.client
import json
import urllib


def main():
    headers = {
        'authorization': "Bearer z-Au8pBkS2rHXt16F4KTR8COP7zRTjurJ39DSAwoyEnBKVriHqOoZgOknYglvLeInXs6tC0Sj4K1bPZctWlMcx6M4pUNcJE4crTg3UoAEfQuoDqEGjQltmKbQHv4WnYx",
        'cache-control': "no-cache",
        'postman-token': "z-Au8pBkS2rHXt16F4KTR8COP7zRTjurJ39DSAwoyEnBKVriHqOoZgOknYglvLeInXs6tC0Sj4K1bPZctWlMcx6M4pUNcJE4crTg3UoAEfQuoDqEGjQltmKbQHv4WnYx"
        }
    conn = http.client.HTTPSConnection("api.yelp.com")
    yelp_biz_id = get_business_d(conn, headers)
    reviews = get_reviews(yelp_biz_id, conn, headers)
    print(reviews)

# get business id from search results
def get_business_d(conn, headers):
    #need the following parameters (type dict) to perform business search.
    params = {'name':'Mexican Post', 'address1':'10 Schalks Crossing Rd', 'city':'Plainsboro', 'state':'NJ', 'country':'US'}

    param_string = urllib.parse.urlencode(params)
    conn.request("GET", "/v3/businesses/matches/best?"+param_string, headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))

    return data['businesses'][0]['id']

# get reviews from business id
def get_reviews(b_id, conn, headers):
    # GET https://api.yelp.com/v3/businesses/{id}/reviews
    # https://api.yelp.com/v3/businesses/YRvBQeFA9s4ekJcsf0Yew/reviews
    r_url = "/v3/businesses/" + b_id + "/reviews"  # review request URL creation based on business ID
    conn.request("GET", r_url, headers=headers)
    rev_res = conn.getresponse()  # response and read functions needed else error(?)
    rev_data = rev_res.read()
    # yelp_reviews = json.loads(rev_data.decode("utf-8"))
    yelp_reviews = []
    for revw in json.loads(rev_data.decode("utf-8"))['reviews']:
        yelp_reviews.append(revw['text'])

    return yelp_reviews

if __name__ == "__main__":
    main()
