__author__ = 'jpatdalton'


import twitter
import columns


access_token = '25019519-qtJxJOLiNEiBt7Cwu4w9jzzXhGvzK8e0QZP1ZwnxM'
access_token_secret = 'GdabupT4MfE6zkGcxGMSMFQmsIM49HVTuYBxoTMcZRJGv'
consumer_secret = 'hdBcUojJveQcFfBIWfytvDPCYJBIfIcP5cv7YE2zATxmMREzlT'
consumer_key = 'DMazZZHzFk2UjBmFt9yuugqeo'


def get_twitter_stats(artists, worksheet, end):

    api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token,
                          access_token_secret=access_token_secret)
    col = columns.twitter
    cell_list_likes = worksheet.range(col+'3:' + col+end)
    for n in xrange(len(artists)):
        name = artists[n]
        try:
            result = api.GetUsersSearch(name,1,1)
            user_id = result[0].id
            user = api.GetUser(user_id)
            if user.verified:
                followers = user.followers_count
            else:
                print 'No verified Twitter account for ' + name
                followers = 'No verified account'
            cell_list_likes[n].value = followers
        except Exception, e:
            print e, 'Twitter Exception on artist [' + name + ']'

    worksheet.update_cells(cell_list_likes)