__author__ = 'jpatdalton'

import urllib2
import json
import facebook
import requests
import columns
import db_setup

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
        except Exception, e:
            print 'JSON error ', e
            return "JSON error"

    except Exception, e:
        print 'not JSON error ', e
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason

def get_page_id(name):
    the_id = 'None'
    try:
        api_endpoint = "https://graph.facebook.com/search?q=" + name + "&type=page" + '&access_token='+ access_token
        data = requests.get(api_endpoint).json()["data"]
        the_id = data[0]["id"]
    except Exception, e:
        print 'Cant get Facebook Id for artist: ' + name
    return the_id

def get_fb_likes(page_id):
    the_likes='None'
    try:
        data = get_page_data(page_id)
        the_likes = str(data['likes'])
    except Exception, e:
        print e, 'Error in get_fb_likes'
    return the_likes

def get_likes(artists, worksheet, end):
    col = columns.fb_likes
    cell_list_likes = worksheet.range(col+'2:'+col+end)
    for n in xrange(len(artists)):
        try:
            page_id = get_page_id(artists[n])
            data = get_page_data(page_id)
            cell_list_likes[n].value = str(data['likes'])
        except Exception, e:
            print e, ' Facebook error ', artists[n]
    worksheet.update_cells(cell_list_likes)
