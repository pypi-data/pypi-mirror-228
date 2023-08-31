from pydantic import BaseModel, Field

from ..util import time as time_lib


class BaseData(BaseModel):
    """
    通用基础数据模型
    """
    # mongodb主键
    _id: str = None
    # 插入时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )
