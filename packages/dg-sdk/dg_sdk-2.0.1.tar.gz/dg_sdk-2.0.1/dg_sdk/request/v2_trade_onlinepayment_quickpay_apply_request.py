from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TRADE_ONLINEPAYMENT_QUICKPAY_APPLY



class V2TradeOnlinepaymentQuickpayApplyRequest(object):
    """
    快捷支付申请
    """

    # 请求日期
    req_date = ""
    # 请求流水号
    req_seq_id = ""
    # 商户号
    huifu_id = ""
    # 订单金额
    trans_amt = ""
    # 绑卡id
    card_bind_id = ""
    # 异步通知地址
    notify_url = ""
    # 用户客户号
    user_huifu_id = ""
    # 安全信息
    risk_check_data = ""
    # 设备数据
    terminal_device_data = ""
    # 银行扩展字段
    extend_pay_data = ""

    def post(self, extend_infos):
        """
        快捷支付申请

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_date":self.req_date,
            "req_seq_id":self.req_seq_id,
            "huifu_id":self.huifu_id,
            "trans_amt":self.trans_amt,
            "card_bind_id":self.card_bind_id,
            "notify_url":self.notify_url,
            "user_huifu_id":self.user_huifu_id,
            "risk_check_data":self.risk_check_data,
            "terminal_device_data":self.terminal_device_data,
            "extend_pay_data":self.extend_pay_data
        }
        required_params.update(extend_infos)
        return request_post(V2_TRADE_ONLINEPAYMENT_QUICKPAY_APPLY, required_params)
