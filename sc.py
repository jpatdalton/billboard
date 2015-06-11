__author__ = 'jpatdalton'

import soundcloud
import requests
import columns

YOUR_CLIENT_ID = 'c95e1781cd020bfb26b72024f50bbbed'
YOUR_CLIENT_SECRET = 'fda9107818d27f857bcafeee668862db'

def get_followers(artists, worksheet, end):

    client = soundcloud.Client(client_id=YOUR_CLIENT_ID,client_secret=YOUR_CLIENT_SECRET)
    col = columns.soundcloud
    cell_list_likes = worksheet.range(col+'2:'+col+end)

    for n in xrange(len(artists)):
        name = artists[n]
        req = 'https://api.soundcloud.com/users.json?q='+name+'&client_id='+YOUR_CLIENT_ID
        try:
            users = requests.get(req).json()
            followers = users[0]["followers_count"]
            cell_list_likes[n].value = followers
        except Exception, e:
            print e, 'Soundcloud couldnt get user ['+name+']'

    worksheet.update_cells(cell_list_likes)

def get_num_followers(id):
    count = 0
    try:
        req = 'https://api.soundcloud.com/users/'+str(id)+'.json?client_id='+YOUR_CLIENT_ID
        user = requests.get(req).json()
        count = user["followers_count"]
    except Exception, e:
        print e, 'soundcloud followers error ', id
    return count


def get_id(name):
    the_id = 'None'
    try:
        req = 'https://api.soundcloud.com/users.json?q='+name+'&client_id='+YOUR_CLIENT_ID
        users = requests.get(req).json()
        the_id = users[0]["id"]
    except Exception, e:
        print e, 'Cant get Soundcloud id for artist: ' + name
    return the_id