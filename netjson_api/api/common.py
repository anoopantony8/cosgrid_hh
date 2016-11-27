

def get_accounts(request):
    accounts_list = []
    try:
        vnf_clouds = sum([[y.cloudid for y in i.policy if
                            y.cloudid.platform == 'netjson'] for i in request.user.roles], [])
        for cloud in vnf_clouds:
            if cloud.name != request.user.cnextname:
                accounts_list.append((cloud.id,cloud.name))
    except Exception ,e:
        print e
        return accounts_list
    return accounts_list

