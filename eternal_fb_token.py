# http://blog.lwolf.org/post/2014-06-16-obtaining-never-expiring-access-token-to-post-on-facebook-page/

# Facebook SDK
import facebook

short_token = ''
client_id = ''
client_secret = ''

# Init graphAPI with short-lived token
graph = facebook.GraphAPI(short_token)

# Exchange short-lived-token to long-lived
long_token = graph.extend_access_token(client_id, client_secret)

# Init graphAPI with long-lived token
graph = facebook.GraphAPI(long_token['access_token'])

# Request all pages for user
pages = graph.get_object('me/accounts')

for page in pages['data']:
    print(page)
