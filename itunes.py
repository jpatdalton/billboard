__author__ = 'jpatdalton'
import requests
import columns
from datetime import date, datetime

def get_song_id(name):
    the_id = 'None'
    try:
        api_endpoint = 'https://itunes.apple.com/search?term='+ name + '&limit=1'
        data = requests.get(api_endpoint).json()["results"]
        the_id = data[0]["trackId"]
    except Exception, e:
        print e, "Itunes id ", name
    return the_id

def get_release_date(id):
    release_date = 'None'
    try:
        user_endpoint = 'https://itunes.apple.com/lookup?id=' + str(id)
        release_date = requests.get(user_endpoint).json()["results"][0]["releaseDate"]
    except Exception, e:
        print e, "Itunes release date", id
    return release_date


def calculate_days_from_release(release_date):
    dt = datetime.today()
    fd = dt.strftime("%m-%d-%y")
    title = fd
    rd = datetime.strptime(release_date, '%Y-%m-%dT%H:%M:%SZ')
    delta = dt - rd
    return delta.days

def get_rd(id):
    return calculate_days_from_release(get_release_date(id))

def itunes_search(titles, worksheet, indices, end):
    col = columns.release_date
    cell_list_dates = worksheet.range(col+'2:'+col+end)
    n=0
    for ind in indices:
        name = titles[n]
        id = get_song_id(name)
        cell_list_dates[ind].value = calculate_days_from_release(get_release_date(id))
        n+=1

    worksheet.update_cells(cell_list_dates)