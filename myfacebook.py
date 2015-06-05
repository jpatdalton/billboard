__author__ = 'jpatdalton'

import urllib2
import json
import facebook
import requests
import columns

APP_SECRET = 'de0ef4983d919423425e08ef6716b66e'
APP_ID = '1105606712786170'
client_token = '8f37afb961d3f2264ad736a94fa546ce'
access_token = '1105606712786170|N51rfQuMviEjoIlqmBdGzZShes8'
#access_token = 'CAACEdEose0cBACZA5EcHTRdGfPeRBXnqfvCG8VSeK3GiehuiE2YfzRvuY9co8OzEoW8SEKqn3zsoqqKZC8Sf6ZAdF7SsRodLY2Ne7fFG0yvbwMNnUHYBZCZA8kLZBFgVgLDHlZAUYBf8ZAck26MjYdZAlRkvkcThbO0SkrqogjjfdMWpGxVJZAJOgUR4T9OmBNmMUcAdBrZBGAYzE79QIytZAmqsoiYRNbVzLZCezfoVSnW881AZDZD'

def get_page_data(page_id):
    api_endpoint = "https://graph.facebook.com"
    fb_graph_url = api_endpoint+"/"+page_id

    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)

        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON error"

    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason

def get_page_id(name):
    api_endpoint = "https://graph.facebook.com/search?q=" + name + "&type=page" + '&access_token='+ access_token
    #api_endpoint = "https://graph.facebook.com/search?q=" + name + "&type=page" + '&access_token='+APP_ID+'|'+APP_SECRET
    #requests.get(api_endpoint).json()
    data = requests.get(api_endpoint).json()["data"]
    return data[0]["id"]
'''
https://graph.facebook.com/search?q=Wiz Khalifa&type=page
fb_graph_url = 'https://graph.facebook.com/oauth/access_token?client_id=1105606712786170&client_secret=de0ef4983d919423425e08ef6716b66e&grant_type=client_credentials'
r = requests.get(fb_graph_url)
access_token = r.text.split('=')[1]
'''


def get_likes(artists, worksheet, end):
    col = columns.fb_likes
    cell_list_likes = worksheet.range(col+'3:'+col+end)
    for n in xrange(len(artists)):
        try:
            page_id = get_page_id(artists[n])
            data = get_page_data(page_id)
            cell_list_likes[n].value = str(data['likes'])
        except Exception, e:
            print e, ' Facebook error ', artists[n]
    worksheet.update_cells(cell_list_likes)
