import os
import facebook

token = os.environ.get('FB_TOKEN')


def get_fb_fans(page_name):
    graph = facebook.GraphAPI(token)
    args = {'fields': 'fan_count'}
    try:
        page_info = graph.get_object(str(page_name), **args)
        return page_info.get('fan_count', 'Чёт ошибочка с подсчётом вышла')
    except facebook.GraphAPIError as e:
        if e.code == 104:
            return 'Что-то с токеном, надо проверить'
        else:
            return 'Неверное имя группы. Может там точку надо поставить или ru добавить?'
