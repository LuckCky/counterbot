# -*- coding: utf-8 -*-

from social_stuff.fb import get_fb_fans
from social_stuff.ok import get_ok_fans
from social_stuff.twi import get_twi_fans
from social_stuff.vk_info import get_vk_fans
from social_stuff.youtube import get_youtube_fans

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
                   "( id SERIAL, projectID INTEGER, projectName VARCHAR(100), " \
                   "resourceName VARCHAR(100),  siteName VARCHAR(15), " \
                   "netAddress VARCHAR(200) ); "
create_users_count_table = "CREATE TABLE usersCount " \
                           "( id SERIAL, " \
                           "projectID INTEGER REFERENCES resourceIds (projectID), " \
                           "date TIMESTAMP, " \
                           "usersCount INTEGER ); "
select_all_aliases = "SELECT * from aliases;"
select_one_from_aliases = "SELECT resourceName from aliases WHERE aliasesList LIKE %s ;"
insert_aliases = "INSERT INTO aliases (resourceName, aliasesList ) VALUES ( %s, %s ) ;"
select_resource_id = "SELECT netAddress FROM resourceIds WHERE resourceName = ( %s ) " \
                     "AND siteName = ( %s )"
insert_resource_ids = "INSERT INTO resourceIds (projectID, projectName, resourceName, siteName, netAddress ) " \
                      "VALUES ( %s, %s, %s, %s, %s ) ;"
select_all_ids = "SELECT * FROM resourceIds;"

# xls with questions
rambler_configs_xls = "utils/Rambler.xls"
aliases_sheet = "Алиасы"
ids_sheet = "Список"

# functions to get number of fans
number_of_fans = {
    "фб": get_fb_fans,
    "вк": get_vk_fans,
    "ок": get_ok_fans,
    "тви": get_twi_fans,
    "ютуб": get_youtube_fans
}
