__author__ = 'jpatdalton'

import spotipy
import columns
import pytesseract
from PIL import Image

def spotify_search(titles, worksheet, indices, end):
    sp = spotipy.Spotify()
    col = columns.spotify_popularity
    cell_list_streams = worksheet.range(col+'2:'+col+end)
    n=0
    for ind in indices:
        results = sp.search(q=titles[n], limit=1)
        cell_list_streams[ind].value = results['tracks']['items'][0]['popularity']
        n+=1
    worksheet.update_cells(cell_list_streams)

def get_id(title):
    the_id = ''
    try:
        sp = spotipy.Spotify()
        results = sp.search(q=title, limit=1)
        the_id = results['tracks']['items'][0]['id']
    except Exception, e:
        print e, 'Cant get Spotify id = ' + title
    return the_id

def get_streams():
    print(pytesseract.image_to_string(Image.open('/Users/jpatdalton/PycharmProjects/billboard/test1.png')))