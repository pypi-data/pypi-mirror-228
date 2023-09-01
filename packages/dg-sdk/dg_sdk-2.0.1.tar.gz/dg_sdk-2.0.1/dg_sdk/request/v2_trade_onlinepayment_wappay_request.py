from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TRADE_ONLINEPAYMENT_WAPPAY



class V2TradeOnlinepaymentWappayRequest(object):
    """
    手机WAP支付
    """

    # 请求日期
    req_date = ""
    # 请求流水号
    req_seq_id = ""
    # 商户号
    huifu_id = ""
    # 交易金额
    trans_amt = ""
    # 网联扩展数据
    extend_pay_data = ""
    # 安全信息
    risk_check_data = ""
    # 设备信息
    terminal_device_data = ""
    # 页面跳转地址
    front_url = ""
    # 异步通知地址
    notify_url = ""

    def post(self, extend_infos):
        """
        手机WAP支付

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_date":self.req_date,
            "req_seq_id":self.req_seq_id,
            "huifu_id":self.huifu_id,
            "trans_amt":self.trans_amt,
            "extend_pay_data":self.extend_pay_data,
            "risk_check_data":self.risk_check_data,
            "terminal_device_data":self.terminal_device_data,
            "front_url":self.front_url,
            "notify_url":self.notify_url
        }
        required_params.update(extend_infos)
        return request_post(V2_TRADE_ONLINEPAYMENT_WAPPAY, required_params, need_verfy_sign=False)
