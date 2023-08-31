# _*_coding:utf-8_*_

import os, logging, time, json, copy

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from xj_finance.utils.utility_method import extract_values, replace_key_in_dict, replace_key_in_list_dicts, \
    replace_key_in_dict_replacement_dicts
from xj_thread.services.thread_list_service import ThreadListService
from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.services.user_service import UserService
from ..services.finance_labor_service import FinanceLaborService
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper, format_params_handle
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_finance.services.finance_transacts_service import FinanceTransactsService
from xj_finance.services.finance_list_service import FinanceListService
from xj_finance.utils.user_wrapper import user_authentication_wrapper
from ..utils.model_handle import util_response
from ..services.finance_service import FinanceService

logger = logging.getLogger(__name__)


class FinanceLaborApi(APIView):  # 或继承(APIView)

    # 资金添加（劳务通）
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def larbor_add(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        transact_set, err = FinanceLaborService.larbor_add(params)
        if err is None:
            return util_response(data=transact_set)
        return util_response(err=47767, msg=err)

    # 资金分配（劳务通）
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def allocated_amount(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        transact_set, err = FinanceLaborService.allocated_amount(params)
        if err is None:
            return util_response(data=transact_set)
        return util_response(err=47767, msg=err)

    # 滞留资金审核（劳务通）
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def detention_review(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        transact_set, err = FinanceLaborService.detention_review(params)
        if err is None:
            return util_response(data=transact_set)
        return util_response(err=47767, msg=err)