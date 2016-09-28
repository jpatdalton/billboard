__author__ = 'jpatdalton'


#!/usr/bin/python
#from urllib import urlencode
#import apiclient
#import apiclient,httplib2, oauth2client, uritemplate
from apiclient.discovery import build
import columns
from apiclient.errors import HttpError
#from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(song_titles, worksheet, indices, end):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                  developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  col = columns.youtube
  cell_list_views = worksheet.range(col+'2:'+col+end)
  n=0
  for ind in indices:
    search_response = youtube.search().list(
      q=song_titles[n],
      part="id",
      maxResults=1
    ).execute()

    search_result = search_response.get("items", [])[0]
    vid_id = search_result["id"]["videoId"]

    # Call the videos.list method to retrieve location details for each video.
    video_response = youtube.videos().list(
      id=vid_id,
      part='statistics',
      maxResults=1
    ).execute()
    cell_list_views[ind].value = video_response["items"][0]["statistics"]["viewCount"]
    n+=1

  worksheet.update_cells(cell_list_views)


youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                  developerKey=DEVELOPER_KEY)

def get_views(vid_id):
    views = 0
    try:
        video_response = youtube.videos().list(
              id=vid_id,
              part='statistics',
              maxResults=1
            ).execute()
        views = video_response["items"][0]["statistics"]["viewCount"]
    except Exception, e:
        print e, 'Youtube Get Views', vid_id
    return views

def get_id(title):
    vid_id = 'None'
    try:
        #youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        #                developerKey=DEVELOPER_KEY)
        search_response = youtube.search().list(
            q=title,
            part="id",
            maxResults=1
          ).execute()
        search_result = search_response.get("items", [])[0]
        vid_id = search_result["id"]["videoId"]

    except Exception, e:
        print 'Cant get Youtube Id for ' + title
    return vid_id

'''
if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
'''