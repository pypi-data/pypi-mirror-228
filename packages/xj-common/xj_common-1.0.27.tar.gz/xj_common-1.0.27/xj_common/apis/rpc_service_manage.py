# encoding: utf-8
"""
@project: djangoModel->rpc_service_manage
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: RPC 调用测试
@created_time: 2023/8/15 8:43
"""
from rest_framework.views import APIView

from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.service_manager import ServiceManager

service_manager = ServiceManager()


class RpcServiceAPIS(APIView):
    @request_params_wrapper
    def get(self, *args, request_params, **kwargs):
        service_id = request_params.get("service_id")
        services, err = service_manager.find_rpc_service(service_id=service_id)
        result = services.hello()
        return util_response(data=result, err=err)
