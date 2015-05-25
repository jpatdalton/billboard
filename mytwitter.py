__author__ = 'jpatdalton'


import twitter


access_token = '25019519-qtJxJOLiNEiBt7Cwu4w9jzzXhGvzK8e0QZP1ZwnxM'
access_token_secret = 'GdabupT4MfE6zkGcxGMSMFQmsIM49HVTuYBxoTMcZRJGv'
consumer_secret = 'hdBcUojJveQcFfBIWfytvDPCYJBIfIcP5cv7YE2zATxmMREzlT'
consumer_key = 'DMazZZHzFk2UjBmFt9yuugqeo'


def get_twitter_stats(artists, worksheet):

    api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token,
                          access_token_secret=access_token_secret)

    cell_list_likes = worksheet.range('M3:M102')
    for n in xrange(100):
        name = artists[n]
        try:
            result = api.GetUsersSearch(name,1,1)
            user_id = result[0].id
            user = api.GetUser(user_id)
            followers = user.followers_count
            cell_list_likes[n].value = followers
        except Exception, e:
            print e, 'Twitter Exception on artist [' + name + ']'

    worksheet.update_cells(cell_list_likes)