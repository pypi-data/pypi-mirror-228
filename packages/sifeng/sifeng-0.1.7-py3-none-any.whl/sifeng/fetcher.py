from joblib import Parallel, delayed
import requests
import pandas as pd
import json
import math
from copy import deepcopy

base_url = "https://service-b6ozb2zl-1300348397.sh.apigw.tencentcs.com/"

def query_size(api, **kwargs):
    api_map = {
        "stock/basic_info": (0, "basic_info"),
        "stock/kline_day": (2, "kline_day"),
        "stock/indicator_day": (2, "indicator_day")
    }
    kwargs = kwargs.copy()
    kwargs["table_type"] = api_map[api][0]
    kwargs["table_name"] = api_map[api][1]
    response = requests.request("GET", base_url + "stock/table_count", params=kwargs, timeout=35)
    response_json = json.loads(response.text)
    return response_json["result"], response_json["partition_len"]

def query(api, fields="*", workers=16, verbose=8, **kwargs):
    """
        Query the distant server and retrieve information.
    """
    if api == "ping":
        response = requests.request("GET", base_url + api, params=kwargs, timeout=25)
        return json.loads(response.text)["response"]
    api_map = {
        "stock/basic_info": ["stock_code", "list_status", "st_flag", "list_date", "industry", "sector", "area", "stock_name"],
        "stock/kline_day": ["stock_code", "trade_date", "open", "high", "low", "close", "vol", "amount", "adj_factor"],
        "stock/indicator_day": ["trade_date", "stock_code", "turnover_rate", "turnover_rate_free", "volume_ratio", "pe", "pe_ttm", "pb", "ps", "ps_ttm", "dv_ratio", "dv_ttm", "total_share", "float_share", "free_share", "total_mv", "circ_mv"]
    }
    if "limit" in kwargs.keys() or "offset" in kwargs.keys():
        kwargs["fields"] = api_map[api] if fields == "*" else fields
        response = requests.request("GET", base_url + api, params=kwargs, timeout=35)
        response_json = json.loads(response.text)
        if response.status_code != 200:
            raise Exception(response.text)
        else:
            return pd.DataFrame(data=response_json["result"], columns=kwargs["fields"])
    else:
        def query(begin_date, end_date, idx):
            params = deepcopy(kwargs)
            params["limit"] = 10000
            params["offset"] = idx * 10000
            params["begin_date"] = begin_date
            params["end_date"] = end_date
            response = requests.get(base_url + api, params=params, timeout=35)
            if response.status_code != 200:
                raise Exception(response.text)
            response_json = json.loads(response.text)
            return pd.DataFrame(data=response_json["result"], columns=kwargs["fields"])
        tasks = []
        table_size, partition_len = query_size(api=api, **kwargs)
        kwargs["fields"] = api_map[api] if fields == "*" else fields
        for year in range(pd.to_datetime(kwargs["begin_date"]).year, pd.to_datetime(kwargs["end_date"]).year + 1, 1):
            begin_date = max(f"{year}-01-01", kwargs["begin_date"])
            end_date = min(kwargs["end_date"], f"{year}-12-31")
            for _ in range(0, math.ceil(partition_len[year - 2000] / 10000), 1):
                tasks.append(delayed(query)(begin_date, end_date, _))
        response = Parallel(n_jobs=workers, verbose=verbose, pre_dispatch=workers)(tasks)
        return pd.concat(response, ignore_index=True)
