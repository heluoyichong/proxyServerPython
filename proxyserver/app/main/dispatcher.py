from proxyserver.app.api.account import AccountAPI


def dispatcher(request):
    return AccountAPI.item_all(request)
