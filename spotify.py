__author__ = 'jpatdalton'

import spotipy
import columns

def spotify_search(titles, worksheet, indices, end):
    sp = spotipy.Spotify()
    col = columns.spotify_popularity
    cell_list_streams = worksheet.range(col+'3:'+col+end)
    n=0
    for ind in indices:
        results = sp.search(q=titles[n], limit=1)
        cell_list_streams[ind].value = results['tracks']['items'][0]['popularity']
        n+=1
    worksheet.update_cells(cell_list_streams)
