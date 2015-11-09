from django.http import JsonResponse
import json


def analyse_post_data(request):
    content_type = request.META['CONTENT_TYPE']
    if "x-www-form-urlencoded" in content_type:
        # Data posted is a dictionary (QueryDict)
        return request.POST
    elif "json" in content_type:
        return json.loads(request.body.decode("utf-8"))


class StatusCode(object):
    # successful
    OK = 200
    CREATED = 201
    # NO_CONTENT = 204
    DELETED = 200
    # unsuccessful
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    DUPLICATED = 409


class ErrorMessage(object):

    @classmethod
    def duplicated(cls):
        return "duplicated record"

    @classmethod
    def not_found(cls):
        return "record not found"

    @classmethod
    def method_not_allowed(cls):
        return "method not allow"

    @classmethod
    def deleted(cls):
        return "record deleted"


class Response(object):

    @classmethod
    def success(cls, message, status_code):
        response = JsonResponse({"status": "success", "data": message})
        response.status_code = status_code
        return response

    @classmethod
    def fail(cls, message, status_code):
        response = JsonResponse({"status": "fail", "error": message})
        response.status_code = status_code
        return response


class get_item_by_id(object):
    def __init__(self, model_name, item_id):
        self.item_id = item_id
        self.model_name = model_name

    def __enter__(self):
        # get the target object
        try:
            return True, self.model_name.objects.get(id=self.item_id)
        except self.model_name.DoesNotExist:
            return False, None

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


##############
# Deprecated #
##############
# class json_message(json):
#     def __init__(self, message):
#         self.message = message
#
#     def read_as_json(self):
#         return self.message

# def response_with_status(message, response_code, status):
#     if status:
#         response = JsonResponse({"status": "success", "data": message})
#     else:
#         response = JsonResponse({"status": "fail", "error": message})
#     response.status_code = response_code
#     return response
