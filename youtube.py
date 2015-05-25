__author__ = 'jpatdalton'


#!/usr/bin/python
#from urllib import urlencode
#import apiclient
#import apiclient,httplib2, oauth2client, uritemplate
from apiclient.discovery import build
from apiclient.errors import HttpError
#from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBUsBv64GNUH77pydLRvHbebR1n57GGbzU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(song_titles, worksheet):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                  developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  cell_list_views = worksheet.range('F3:F102')
  for n in xrange(100):
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
      part='statistics'
    ).execute()
    cell_list_views[n].value = video_response["items"][0]["statistics"]["viewCount"]
  worksheet.update_cells(cell_list_views)

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