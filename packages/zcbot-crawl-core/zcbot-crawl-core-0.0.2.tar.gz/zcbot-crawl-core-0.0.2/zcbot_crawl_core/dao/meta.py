# -*- coding: utf-8 -*-
from typing import List
from ..client.mongo_client import Mongo


# 获取链接分拣规则配置
def get_url_parse_rule(host: str = None):
    if host:
        return Mongo().get('zcbot_url_parse_rule', {'_id': host})

    return Mongo().list('zcbot_url_parse_rule')


# 获取支持网站平台
def get_platforms():
    return Mongo().list('zcbot_platforms', sort=[('sort', 1)])

