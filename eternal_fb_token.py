# http://blog.lwolf.org/post/2014-06-16-obtaining-never-expiring-access-token-to-post-on-facebook-page/

# Facebook SDK
import facebook

short_token = 'EAAJbABiT2nMBANjPVmWDwDfJR8ZBZAhxyKpiwbbxtgcjx1GdZAobcWjDMEh7krP7qNn0ZCR6hAwZApcyuCsolQf5jbnZA1F0h6LlVWz91d0kXsPPZAaQoPyzah4LvPUDfZBAciaRGJYFkXepxzXM1wZBuWuXlDSNweuJypsSJcgHz8iZB7ZA04PWcDdwaygrgmDLUUZD'
client_id = '663005923891827'
client_secret = '006135fcf69bf5cd058f99d51d915056'

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
