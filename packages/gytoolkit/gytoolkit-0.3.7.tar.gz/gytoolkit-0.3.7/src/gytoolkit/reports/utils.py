import os
from typing import List
import pandas as pd
from .constants import NetValueData


def clean_up_otc_netvalues(otc_netvalues: pd.DataFrame) -> List[NetValueData]:
    """
    清理OTC净值数据，并返回NetValueData对象列表。

    参数:
        otc_netvalues (pd.DataFrame): 包含OTC净值数据的DataFrame。

    返回:
        List[NetValueData]: NetValueData对象列表。

    """
    netvalue_list = []
    for row in otc_netvalues.itertuples():
        date = row.净值日期
        prodcode = row.产品编码
        prodname = row.产品简称
        netvalue = row.最新净值
        cum_netvalue = row.累计净值
        netvalue_list.append(
            NetValueData(
                date=date,
                prodcode=prodcode,
                prodname=prodname,
                netvalue=netvalue,
                cum_netvalue=cum_netvalue,
            )
        )
    return netvalue_list


def update_local_net_values(
    new_net_values: List[NetValueData], cachedir: str = None
) -> None:
    """
    更新本地净值数据，使用给定的新净值数据。

    参数:
        new_net_values (List[NetValueData]): 需要更新的新净值数据列表。
        cachedir (str): 缓存目录的路径。如果未提供，则默认使用当前目录下的".cache/"目录。

    返回:
        None: 此函数不返回任何内容。
    """
    # 如果未提供缓存目录，则使用默认路径
    if cachedir is None:
        cachedir = "./.cache/"

    # 如果缓存目录不存在，则创建
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    # 将新净值数据转换为DataFrame，并设置索引
    if len(new_net_values) > 0:
        new_net_values = pd.DataFrame(new_net_values).set_index(["date", "prodcode"])

    try:
        # 从feather文件中读取本地净值数据，并设置索引
        local_net_values = pd.read_feather(cachedir + "net_values.feather").set_index(
            ["date", "prodcode"]
        )
    except:
        local_net_values = None

    if local_net_values is not None:
        # 将新净值数据与本地净值数据合并，替换缺失值
        new_net_values = new_net_values.combine_first(local_net_values)

    # 按日期升序、产品代码升序排序新净值数据
    new_net_values.sort_index(ascending=[True, True]).reset_index().to_feather(
        cachedir + "net_values.feather"
    )

def update_tradings_days():
    jq.get_tradings_days()