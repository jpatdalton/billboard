__author__ = 'jpatdalton'



import urllib2
import json
import facebook
import requests

APP_SECRET = 'de0ef4983d919423425e08ef6716b66e'
APP_ID = '1105606712786170'
client_token = '8f37afb961d3f2264ad736a94fa546ce'
access_token = '1105606712786170|N51rfQuMviEjoIlqmBdGzZShes8'

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


'''
graph = facebook.GraphAPI(access_token=access_token)
graph.request('/search')

'''



def get_likes(artists, worksheet):

    cell_list_likes = worksheet.range('J3:J102')
    for n in xrange(100):
        page_id = get_page_id(artists[n])
        data = get_page_data(page_id)
        cell_list_likes[n].value = str(data['likes'])

    worksheet.update_cells(cell_list_likes)
