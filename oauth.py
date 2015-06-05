__author__ = 'jpatdalton'

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from datetime import date

#TODO: create and archive spreadsheets on the go with gdata api
def open_worksheet():
    json_key = json.load(open('billboard-159a437cff31.json'))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)
    #dt = date.today()

    #fd = dt.strftime("%m-%d-%Y")
    #title = 'Live Metrics ' + fd
    title = 'Live Metrics 06-04-15'
    wks = gc.open(title)


    worksheet = wks.sheet1

    print worksheet.title

    return worksheet


