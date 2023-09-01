import decimal
import json
import sys
import time
from datetime import timedelta
from pathlib import Path
from decimal import Decimal
import math
import random
from uuid import uuid4

from django.core.cache import cache
from django.db.models import Q
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.datetime_safe import datetime
import pytz
from numpy.core.defchararray import upper
from main.settings import BASE_DIR
from xj_user.services.user_bank_service import UserBankCardsService
from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.services.user_service import UserService
from .finance_transact_service import FinanceTransactService
from ..models import Transact
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
import os


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, int):
                return int(obj)
            elif isinstance(obj, float) or isinstance(obj, decimal.Decimal):
                return float(obj)
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, datetime.date):
                return obj.strftime('%Y-%m-%d')
            if isinstance(obj, time) or isinstance(obj, timedelta):
                return obj.__str__()
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as e:
            # logger.exception(e, stack_info=True)
            return obj.__str__()


class FinanceLaborService:

    # 资金数据写入服务
    @staticmethod
    def larbor_add(params):
        data = []
        order_no = params.get('order_no', "")  # 订单号
        account_id = params.get("account_id", "")  # 账户
        their_account_id = params.get("their_account_id", "")  # 对方账户
        their_account_bank_card_id = params.get("their_account_bank_card_id", "")  # 入账银行
        transact_time = params.get("transact_time", "")  # 汇入时间
        amount = params.get("amount", "")  # 汇入金额
        remark = params.get("remark", "")  # 扣款依据（备注）
        manage_point = params.get("manage_point", "")  # 管理费点数
        management_fees = params.get("management_fees", "")  # 管理费金额
        tax_point = params.get("tax_point", "")  # 税金点数
        taxes = params.get("taxes", "")  # 税金
        brokerage_point = params.get("brokerage_point", "")  # 佣金点数
        commission = params.get("commission", "")  # 佣金
        # amount_remitted = params.get("amount_remitted", "")  # 汇出金额
        # remit_time = params.get("remit_time", "")  # 汇出时间
        images = params.get("images", "")  # 凭证照片
        collection = params.get("collection", "")  # 收款列表
        info_data = {
            'account_id': account_id,
            'their_account_id': their_account_id,
            'relate_uuid': uuid4(),
            'order_no': order_no,
            'bookkeeping_type': "TRANSACT"  # 交易行为
        }

        # 汇入数据
        import_data = info_data.copy()
        import_data['transact_time'] = transact_time
        import_data['amount'] = abs(Decimal(amount))
        import_data['remark'] = remark
        import_data['bookkeeping_type'] = "OFFLINE"  # 转账行为
        data.append(import_data)

        if not order_no:
            import_data['sand_box'] = "RETENTION"

        if manage_point:
            # 管理费数据
            manage_data = info_data.copy()
            manage_data['manage_point'] = manage_point
            manage_data['amount'] = -abs(Decimal(management_fees))
            manage_data['sand_box'] = "MANAGEMENT_FEE_RECEIVABLE"
            data.append(manage_data)
        if tax_point:
            # 税金数据
            taxes_data = info_data.copy()
            taxes_data['tax_point'] = tax_point
            taxes_data['amount'] = -abs(Decimal(taxes))
            taxes_data['sand_box'] = "TAX_RECEIVABLES"
            data.append(taxes_data)
        if brokerage_point:
            # 佣金数据
            commission_data = info_data.copy()
            commission_data['tax_point'] = brokerage_point
            commission_data['amount'] = -abs(Decimal(commission))
            commission_data['sand_box'] = "COMMISSION_RECEIVABLE"
            data.append(commission_data)

        if collection:
            # 汇出数据
            for i in collection:
                if not i.get("their_account_id", ""):
                    # 2、检查客户是否在系统中有录入
                    user_name, err = DetailInfoService.get_detail(
                        search_params={"nickname": i.get("nickname", "")})
                    if user_name:
                        user_id = user_name['user_id']
                    else:
                        # 3、如果不存在该客户创建（不用登录的客户,不会隶属于组织结构，会绑定到企业账号旗下）（甲方）
                        user, user_err = UserService.user_add({
                            'nickname': i.get("nickname", ""),
                            'full_name': i.get("nickname", ""),
                            'user_type': "PAYEE"
                        })
                        if user_err:
                            return None, "录入失败"
                        user_id = user['user_id']
                    # 4、如果银行卡卡号不存在
                    user_bank, user_bank_err = UserBankCardsService.get_bank_card(
                        {"bank_card_num": i.get("bank_card_num", "")})
                    if not user_bank['list']:
                        user_bank_add, user_bank_err_add = UserBankCardsService.add({
                            "user_id": user_id,
                            "bank_card_num": i.get("bank_card_num", ""),
                            "open_account_bank": i.get("open_account_bank", ""),
                            "is_default": 1,
                            "remark": "",
                            "ext": {}
                        })
                        their_account_bank_card_id = user_bank_add['id']
                    else:
                        their_account_bank_card_id = user_bank['list'][0]['id']

                remit_data = info_data.copy()
                remit_data['their_account_bank_card_id'] = their_account_bank_card_id
                remit_data['their_account_id'] = user_id
                remit_data['amount'] = -abs(Decimal(i['amount_remitted']))
                data.append(remit_data)

        try:
            for item in data:
                thread, thread_err = FinanceTransactService.add(item)
                if thread_err:
                    return None, thread_err
        except Exception as e:
            return None, str(e)

        print(data)
        return None, None

    @staticmethod
    def allocated_amount(params):
        finance_id = params.get("finance_id", "")  # 要分配的滞留资金id
        contract_code = params.get("contract_code", "")  # 合同编码
        remittance_amount = params.get("remittance_amount", "")  # 汇入金额
        transact_set = Transact.objects.filter(id=finance_id).first()
        if transact_set:
            transact = model_to_dict(transact_set)

        remit, remit_err = FinanceTransactService.add({
            'account_id': transact.get("account_id", ""),
            'their_account_id': transact.get("their_account_id", ""),
            'relate_uuid': transact.get("relate_uuid", ""),
            'order_no': contract_code,
            'bookkeeping_type': "TRANSACT",  # 交易行为
            "amount": Decimal(remittance_amount),
            "transact_time": transact.get("remittance_time", ""),
            "sand_box": "DETENTION_REVIEW"
        })
        if remit_err:
            return None, remit_err
        return None, None

    @staticmethod
    def detention_review(params):
        finance_id = params.get("finance_id", "")  # 要审核的滞留资金id
        detention_review_set = Transact.objects.filter(id=finance_id).first()
        detention_review = model_to_dict(detention_review_set)

        filter = {
            "relate_uuid": detention_review['relate_uuid'],
            "sand_box__sand_box_name": "RETENTION"
        }
        retention_set = Transact.objects.filter(**filter).first()
        retention = model_to_dict(retention_set)

        post_allocation = Decimal(retention['income']) - Decimal(detention_review['income'])
        update_data = {
            "income": post_allocation
        }
        if not post_allocation:
            update_data['is_write_off'] = 1

        Transact.objects.filter(id=finance_id).update(**{"is_write_off": 1})
        Transact.objects.filter(**filter).update(**update_data)

        thread, thread_err = FinanceTransactService.add({
            'account_id': detention_review.get("account_id", ""),
            'their_account_id': detention_review.get("their_account_id", ""),
            'relate_uuid': detention_review.get("relate_uuid", ""),
            'order_no': detention_review.get('order_no'),
            'bookkeeping_type': "TRANSACT",  # 交易行为
            "amount": detention_review.get("income"),
            "transact_time": detention_review.get("remittance_time", ""),
        })
        if thread_err:
            return None, thread_err
        return None, None
