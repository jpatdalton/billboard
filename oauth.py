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
import datetime
import sys

#TODO: create and archive spreadsheets on the go with gdata api
def open_spreadsheet():
    json_key = json.load(open('billboard-159a437cff31.json'))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)

    day_of_week = datetime.datetime.today().isoweekday()

    if day_of_week < 2:
        past_tues = datetime.datetime.today() - datetime.timedelta(days = (day_of_week) + 5)
    else:
        past_tues = datetime.datetime.today() - datetime.timedelta(days = (day_of_week) - 2)

    fd = past_tues.strftime("%m-%d-%y")
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
        worksheet_retrieved = wks.add_worksheet(title, 200, 35)
        add_column_headers(worksheet_retrieved)
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
    cell_list = worksheet.range('A1:AC1')
    for cell in cell_list:
        #print cell.col
        cell.value = columns.headers[cell.col-1]
    worksheet.update_cells(cell_list)

'''
import oauth
worksheet = oauth.open_worksheet()

'''

if len(sys.argv) == 2:
    if sys.argv[1] == 'clear':
        print 'clearing worksheet...'
        wks = open_spreadsheet()
        clear_worksheet(wks)