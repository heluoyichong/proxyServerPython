from proxyserver.app.main.models import Account
from proxyserver.app.api.base import BaseAPI
import logging

logger = logging.getLogger("app.debug")


class AccountAPI(BaseAPI):
    @classmethod
    def item_all(cls, request):
        return BaseAPI.item_all(request, Account)

