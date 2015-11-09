from proxyserver.app.main.common import *
import logging

logger = logging.getLogger("app.debug")


class BaseAPI(object):
    @classmethod
    def item_all(cls, request, model_name):
        if request.method == 'GET':
            data_all = {}
            items = model_name.objects.all()
            for item in items:
                data_per = item.read_as_json()
                # Unique ID per host record
                item_id = item.id
                # Append JSON structure per host record to whole result set
                data_all["id_"+str(item_id)] = data_per
            return Response.success(data_all, StatusCode.OK)
        # POST new host record
        elif request.method == 'POST':
                p_data = analyse_post_data(request)
                return model_name.create_as_json(p_data)
        else:
            return Response.fail(ErrorMessage.method_unsupported(), StatusCode.METHOD_NOT_ALLOWED)

