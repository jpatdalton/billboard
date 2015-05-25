__author__ = 'jpatdalton'

import spotipy
sp = spotipy.Spotify()

def spotify_search(titles, worksheet):

    cell_list_streams = worksheet.range('G3:G102')
    for n in xrange(100):
        results = sp.search(q=titles[n], limit=1)

        cell_list_streams[n].value = results['tracks']['items'][0]['popularity']

    worksheet.update_cells(cell_list_streams)
