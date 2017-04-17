import vk


def get_vk_fans(group_name):
    vk.Session()
    session = vk.Session()
    api = vk.API(session)
    try:
        group_info = api.groups.getById(group_id=group_name, fields='members_count')
    except vk.exceptions.VkAPIError as e:
        if e.code == 100:
            return 'Неверное имя группы. Может там точку надо поставить или ru добавить?'
        else:
            return e.message
    try:
        return group_info['members_count']
    except KeyError:
        return None
