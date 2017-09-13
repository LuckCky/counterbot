# -*- coding: utf-8 -*-

from social_stuff.fb import get_fb_fans
from social_stuff.ok import get_ok_fans
from social_stuff.twi import get_twi_fans
from social_stuff.vk_info import get_vk_fans
from social_stuff.youtube import get_youtube_fans
from social_stuff.g_plus import get_g_plus_fans
from social_stuff.inst import get_bloggers

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
                           "projectID INTEGER, " \
                           "date TIMESTAMP, " \
                           "usersCount INTEGER ); "
create_all_users_table = "CREATE TABLE totalUsersCount " \
                         "( id SERIAL, " \
                         "date TIMESTAMP, " \
                         "totalUsersCount INTEGER );"
select_all_aliases = "SELECT * from aliases;"
select_one_from_aliases = "SELECT resourceName from aliases WHERE aliasesList LIKE %s ;"
insert_aliases = "INSERT INTO aliases (resourceName, aliasesList ) VALUES ( %s, %s ) ;"
select_resource_id_by_name = "SELECT netAddress FROM resourceIds WHERE resourceName = ( %s ) " \
                     "AND siteName = ( %s )"
insert_resource_ids = "INSERT INTO resourceIds (projectID, projectName, resourceName, siteName, netAddress ) " \
                      "VALUES ( %s, %s, %s, %s, %s ) ;"
select_all_ids = "SELECT * FROM resourceIds;"
select_all_names_from_aliases = "SELECT resourceName from aliases ;"
select_resource_id_by_project = "SELECT projectID, netAddress FROM resourceIds " \
                                "WHERE projectName = ( %s ) AND siteName = ( %s )"
insert_data = "INSERT INTO usersCount (projectID, date, usersCount )" \
              " VALUES ( %s, %s, %s ) ;"
insert_all_users_data = "INSERT INTO totalUsersCount (date, totalUsersCount) VALUES (%s, %s);"
select_last_users_data = "SELECT * FROM totalUsersCount ORDER BY date DESC limit 1 ; "
select_all_user_per_date = "SELECT * FROM totalUsersCount WHERE date = (%s) ORDER BY date ASC limit 1 ;"

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
    "ютуб": get_youtube_fans,
    "г+": get_g_plus_fans,
    "инст": get_bloggers,
}

network_list = ['фб', 'вк', 'ок', 'тви', 'ютуб', 'г+', 'инст']
