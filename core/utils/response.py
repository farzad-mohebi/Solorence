from rest_framework.exceptions import APIException

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class BadRequest(APIException):
    status_code = 400
    default_detail = 'bad request'
    default_code = 'bad_request'


class ResponseOk(Response):
    def __init__(self, data=None, status=None, detail=None, template_name=None, headers=None, exception=False,
                 content_type=None):
        if not data:
            data = {}
        data['ok'] = True
        if detail:
            data['detail'] = detail
        super().__init__(data, status, template_name, headers, exception, content_type)


class ResponseNotOk(Response):
    def __init__(self, data=None, reason=None, status=None, template_name=None, headers=None, exception=False,
                 content_type=None):
        if not data:
            data = {}
        data['ok'] = False
        if reason:
            data['reason'] = reason
        status = HTTP_400_BAD_REQUEST
        super().__init__(data, status, template_name, headers, exception, content_type)
