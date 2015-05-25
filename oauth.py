__author__ = 'jpatdalton'

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def open_worksheet():
    json_key = json.load(open('billboard-159a437cff31.json'))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)
    try:
        wks = gc.open('Weekly Billboard Metrics Current.xlsx')
    except Exception, e:
        print e

    worksheet = wks.sheet1

    print worksheet.title

    return worksheet


