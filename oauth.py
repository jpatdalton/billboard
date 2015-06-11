__author__ = 'jpatdalton'

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from datetime import date
import httplib2
from apiclient import errors
#from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
import columns

#TODO: create and archive spreadsheets on the go with gdata api
def open_spreadsheet():
    json_key = json.load(open('billboard-159a437cff31.json'))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)
    dt = date.today()

    fd = dt.strftime("%m-%d-%y")
    title = fd
    wks = ''
    try:
        wks = gc.open('Live Metrics')
    except:
        print ''

    worksheetz = wks.worksheets()

    index = -1
    n = 0
    for worksheet in worksheetz:
        if worksheet.title == title:
            index = n
            break
        n+=1
    if index == -1:
        worksheet_retrieved = wks.add_worksheet(title, 200, 25)
        print 'added worksheet ', worksheet_retrieved.title
    else:
        worksheet_retrieved = wks.get_worksheet(index)
        print 'retrieved existing worksheet', worksheet_retrieved.title

    return worksheet_retrieved


def clear_worksheet(worksheet):
    worksheet.spreadsheet.del_worksheet(worksheet)
    new_worksheet = open_spreadsheet()
    add_column_headers(new_worksheet)
    return new_worksheet

def add_column_headers(worksheet):
    cell_list = worksheet.range('A1:B1')
    for cell in cell_list:
        cell.value = columns.headers[cell.col-1]
    worksheet.update_cells(cell_list)

'''
import oauth
worksheet = oauth.open_worksheet()

'''