# -*- coding: utf-8 -*-

# Your own chat id. Ask https://telegram.me/my_id_bot to tell you yours
my_id = ''

# cherrypy server params
webhook_listen = '0.0.0.0'

post_url = 'https://guarded-tundra-24703.herokuapp.com/'

# SQL
create_aliases_table = "CREATE TABLE aliases ( resourceName VARCHAR(50), aliasesList VARCHAR(1000) ); "
create_ids_table = "CREATE TABLE ids " \
                   "( projectID INTEGER, projectName VARCHAR(100), " \
                   "resourceName VARCHAR(100),  siteName VARCHAR(15), " \
                   "netAddress VARCHAR(200) ); "
create_data_table = "CREATE TABLE data " \
                   "( projectID INTEGER, date DATETIME, " \
                   "usersCount INTEGER ); "
