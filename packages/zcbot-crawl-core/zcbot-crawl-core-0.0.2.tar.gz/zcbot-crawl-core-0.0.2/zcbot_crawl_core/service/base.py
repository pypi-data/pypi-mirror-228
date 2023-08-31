# -*- coding: utf-8 -*-
from ..util import logger
from ..dao import meta as meta_dao

LOGGER = logger.get('基础')


# 获取支持网站平台
def get_platforms():
    return meta_dao.get_platforms()


# 获取链接分拣规则配置
def get_url_parse_rule(host: str = None):
    return meta_dao.get_url_parse_rule(host)
