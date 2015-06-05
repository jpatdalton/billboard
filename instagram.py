__author__ = 'jpatdalton'

import requests
import columns

#api_endpoint = 'https://api.instagram.com/v1/users/search?q=Wiz Khalifa&count=1&client_id=784b8821947441119467c6358fe7601b'
client_id = '784b8821947441119467c6358fe7601b'

def get_instas(artists, worksheet, end):
    col = columns.instagram
    cell_list_likes = worksheet.range(col+'3:'+col+end)
    for n in xrange(len(artists)):
        name = artists[n].lower()
        api_endpoint = 'https://api.instagram.com/v1/users/search?q=' + name + '&count=1&client_id=784b8821947441119467c6358fe7601b'
        try:
            #requests.get(api_endpoint).json()
            data = requests.get(api_endpoint).json()["data"]
            id = data[0]["id"]
            api_endpoint_id = 'https://api.instagram.com/v1/users/' + id + '/?client_id=784b8821947441119467c6358fe7601b'
            #requests.get(api_endpoint_id).json()
            cell_list_likes[n].value = requests.get(api_endpoint_id).json()["data"]["counts"]["followed_by"]
        except Exception, e:
            print e, ' Couldnt get insta acct for [' + name + ']'


    worksheet.update_cells(cell_list_likes)
