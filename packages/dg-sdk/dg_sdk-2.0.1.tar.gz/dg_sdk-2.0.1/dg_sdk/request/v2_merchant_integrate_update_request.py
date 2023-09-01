from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_INTEGRATE_UPDATE



class V2MerchantIntegrateUpdateRequest(object):
    """
    商户统一变更接口(2022)
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 汇付ID
    huifu_id = ""
    # 渠道商汇付ID
    upper_huifu_id = ""
    # 业务处理类型
    deal_type = ""

    def post(self, extend_infos):
        """
        商户统一变更接口(2022)

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "upper_huifu_id":self.upper_huifu_id,
            "deal_type":self.deal_type
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_INTEGRATE_UPDATE, required_params)
