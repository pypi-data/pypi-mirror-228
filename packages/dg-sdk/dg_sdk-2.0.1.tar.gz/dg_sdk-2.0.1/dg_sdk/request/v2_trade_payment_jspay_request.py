from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TRADE_PAYMENT_JSPAY



class V2TradePaymentJspayRequest(object):
    """
    聚合正扫接口
    """

    # 请求日期
    req_date = ""
    # 请求流水号
    req_seq_id = ""
    # 商户号
    huifu_id = ""
    # 交易类型
    trade_type = ""
    # 交易金额
    trans_amt = ""
    # 商品描述
    goods_desc = ""

    def post(self, extend_infos):
        """
        聚合正扫接口

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_date":self.req_date,
            "req_seq_id":self.req_seq_id,
            "huifu_id":self.huifu_id,
            "trade_type":self.trade_type,
            "trans_amt":self.trans_amt,
            "goods_desc":self.goods_desc
        }
        required_params.update(extend_infos)
        return request_post(V2_TRADE_PAYMENT_JSPAY, required_params)
