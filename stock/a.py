import akshare as ak
import pandas as pd


def get_etf_list() -> pd.DataFrame:
    """
    获取 ETF 列表（用于查找黄金 ETF 代码）
    """
    return ak.fund_etf_spot_em()


def get_gold_etf_list(keyword: str = "黄金") -> pd.DataFrame:
    """
    筛选“黄金 ETF”列表（按名称关键字匹配）
    返回 fund_etf_spot_em 的子集。
    """
    df = get_etf_list()
    name_col = "名称" if "名称" in df.columns else ("基金简称" if "基金简称" in df.columns else None)
    if name_col is None:
        raise RuntimeError(f"ETF列表缺少名称列，实际列：{list(df.columns)}")
    return df[df[name_col].astype(str).str.contains(keyword, na=False)].reset_index(drop=True)


def get_gold_etf_daily(symbol: str, start_date: str = "19900101", end_date: str = "20991231", adjust: str = "") -> pd.DataFrame:
    """
    获取黄金 ETF 历史日线（东方财富）
    symbol: ETF代码（不带市场前缀），如 518880 / 159934 / 159937

    常见返回列：日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率
    """
    df = ak.fund_etf_hist_em(
        symbol=str(symbol),
        period="daily",
        start_date=str(start_date).replace("-", ""),
        end_date=str(end_date).replace("-", ""),
        adjust=adjust,  # '', 'qfq', 'hfq'
    )
    if "日期" in df.columns:
        df["日期"] = pd.to_datetime(df["日期"])
        df = df.sort_values("日期").reset_index(drop=True)
    return df


if __name__ == "__main__":
    # 1) 找黄金 ETF 代码
    gold_list = get_gold_etf_list()
    print(gold_list.head(20).to_string(index=False))

    # 2) 取其中一只拉日线（示例：518880）
    df = get_gold_etf_daily("518880", start_date="2020-01-01", end_date="2024-12-31", adjust="")
    print(df.head(10).to_string(index=False))