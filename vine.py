__author__ = 'jpatdalton'


import requests


def get_page_id(name):
    api_endpoint = 'https://api.vineapp.com/users/search/' + name
    #api_endpoint = "https://graph.facebook.com/search?q=" + name + "&type=page" + '&access_token='+APP_ID+'|'+APP_SECRET
    data = requests.get(api_endpoint).json()["data"]

    return data["records"][0]["userId"]
def get_user_data(id):
    user_endpoint = 'https://api.vineapp.com/users/profiles/' + str(id)
    data = requests.get(user_endpoint).json()["data"]
    return data['followerCount']


def get_vine_stats(artists, worksheet):

    cell_list_likes = worksheet.range('O3:O102')
    for n in xrange(100):
        name = artists[n]
        try:
            page_id = get_page_id(name)
            data = get_user_data(page_id)
            cell_list_likes[n].value = str(data)
        except Exception, e:
            print e, 'Vine access error ['+name+']'

    worksheet.update_cells(cell_list_likes)