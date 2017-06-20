# -*- coding: utf-8 -*-

# Your own chat id. Ask https://telegram.me/my_id_bot to tell you yours
my_id = ''

# cherrypy server params
webhook_listen = '0.0.0.0'

post_url = 'https://guarded-tundra-24703.herokuapp.com/'

# SQL
create_aliases_table = "CREATE TABLE aliases (" \
                       "id SERIAL, " \
                       "resourceName VARCHAR(50), " \
                       "aliasesList VARCHAR(1000) ); "
create_ids_table = "CREATE TABLE resourceIds " \
                   "( projectID INTEGER, projectName VARCHAR(100), " \
                   "resourceName VARCHAR(100),  siteName VARCHAR(15), " \
                   "netAddress VARCHAR(200) ); "
create_users_count_table = "CREATE TABLE usersCount " \
                   "( projectID INTEGER, date TIMESTAMP, " \
                   "usersCount INTEGER ); "
select_all_aliases = "SELECT * from aliases;"
select_one_from_aliases = "SELECT resourceName from aliases WHERE aliasesList LIKE %(%s)% ;"
insert_aliases = "INSERT INTO aliases (resourceName, aliasesList ) VALUES ( %s, %s ) ;"

# xls with questions
rambler_configs_xls = "utils/Rambler.xls"
aliases_sheet = "Алиасы"
