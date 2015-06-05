__author__ = 'jpatdalton'


import requests
import columns

def get_page_id(name):
    api_endpoint = 'https://api.vineapp.com/users/search/' + name
    #api_endpoint = "https://graph.facebook.com/search?q=" + name + "&type=page" + '&access_token='+APP_ID+'|'+APP_SECRET
    data = requests.get(api_endpoint).json()["data"]

    return data["records"][0]["userId"]
def get_user_data(id):
    user_endpoint = 'https://api.vineapp.com/users/profiles/' + str(id)
    data = requests.get(user_endpoint).json()["data"]
    if data["verified"]:
        return data['followerCount']
    else:
        print str(data['username']) + ' has no verified Vine account'
        return 'No verified account'


def get_vine_stats(artists, worksheet, end):
    col = columns.vine
    cell_list_likes = worksheet.range(col+'3:'+col+end)
    for n in xrange(len(artists)):
        name = artists[n]
        try:
            page_id = get_page_id(name)
            data = get_user_data(page_id)
            cell_list_likes[n].value = str(data)
        except Exception, e:
            print e, 'Vine access error ['+name+']'

    worksheet.update_cells(cell_list_likes)