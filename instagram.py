__author__ = 'jpatdalton'

import requests
import columns

#api_endpoint = 'https://api.instagram.com/v1/users/search?q=Wiz Khalifa&count=1&client_id=784b8821947441119467c6358fe7601b'
client_id = ''

def get_instas(artists, worksheet, end):
    col = columns.instagram
    cell_list_likes = worksheet.range(col+'2:'+col+end)
    for n in xrange(len(artists)):
        name = artists[n].lower()
        api_endpoint = 'https://api.instagram.com/v1/users/search?q=' + name + '&count=1&client_id='
        try:
            #requests.get(api_endpoint).json()
            data = requests.get(api_endpoint).json()["data"]
            id = data[0]["id"]
            api_endpoint_id = 'https://api.instagram.com/v1/users/' + id + '/?client_id='
            #requests.get(api_endpoint_id).json()
            cell_list_likes[n].value = requests.get(api_endpoint_id).json()["data"]["counts"]["followed_by"]
        except Exception, e:
            print e, ' Couldnt get insta acct for [' + name + ']'


    worksheet.update_cells(cell_list_likes)

def get_id(name):
    the_id = 'None'
    try:
        api_endpoint = 'https://api.instagram.com/v1/users/search?q=' + name + '&count=1&client_id='
        data = requests.get(api_endpoint).json()["data"]
        the_id = data[0]["id"]
    except Exception, e:
        print e, 'Cant get Instagram id for artist: ' + name
    return the_id

def get_followers(page_id):
    followers = 0
    try:
        api_endpoint_id = 'https://api.instagram.com/v1/users/' + page_id + '/?client_id='
        followers = requests.get(api_endpoint_id).json()["data"]["counts"]["followed_by"]
    except Exception, e:
        print e, page_id, 'Insta get followers'
    return followers

def get_username(page_id):
    username = ''
    try:
        api_endpoint_id = 'https://api.instagram.com/v1/users/' + page_id + '/?client_id='
        username = requests.get(api_endpoint_id).json()["data"]["username"]
    except Exception, e:
        print e, page_id, 'Insta get username'
    return username