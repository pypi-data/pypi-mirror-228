# -*- coding: utf-8 -*-
from typing import List

from ..util import logger
from ..dao import base as base_dao
from ..model.entity import BatchSpiderGroup

LOGGER = logger.get('基础')


# 获取支持网站平台
def get_platforms():
    return base_dao.get_platforms()


def get_support_spiders_by_group(group_code: str = None, plat_codes: List[str] = None, enable: int = None):
    rows = base_dao.get_spider_group_list(group_code=group_code, plat_codes=plat_codes, enable=enable)
    rows = [BatchSpiderGroup(**x).dict() for x in rows]
    return rows


def get_support_platforms_by_group(group_code: str, enable: int = None):
    rows = base_dao.get_spider_group_list(group_code=group_code, enable=enable)
    rows = [BatchSpiderGroup(**x).dict() for x in rows]
    return rows


# 获取支持网站平台
def get_url_parse_rule(host: str = None):
    return base_dao.get_url_parse_rule(host)
