from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TRADE_PAYSCORE_PAY_PAYSCOREPAY



class V2TradePayscorePayPayscorepayRequest(object):
    """
    支付分扣款
    """

    # 微信扣款单号
    out_trade_no = ""
    # 商品描述
    goods_desc = ""
    # 商户号
    huifu_id = ""
    # 安全信息
    risk_check_data = ""

    def post(self, extend_infos):
        """
        支付分扣款

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "out_trade_no":self.out_trade_no,
            "goods_desc":self.goods_desc,
            "huifu_id":self.huifu_id,
            "risk_check_data":self.risk_check_data
        }
        required_params.update(extend_infos)
        return request_post(V2_TRADE_PAYSCORE_PAY_PAYSCOREPAY, required_params)
