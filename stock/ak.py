"""
A股股票数据获取工具（基于 akshare）
- 获取日线行情（复权/不复权）
- 获取实时行情
- 获取指数日线
- 命令行运行示例见 main()

依赖：
  pip install -U akshare pandas
注意：
  akshare 数据源可能会变动；如接口不可用请升级 akshare 或调整接口参数。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

import pandas as pd

try:
    import akshare as ak
except ImportError as e:
    raise SystemExit("缺少依赖：pip install -U akshare pandas") from e


Adjust = Literal["", "qfq", "hfq"]  # 不复权/前复权/后复权


@dataclass(frozen=True)
class DailyKlineParams:
    symbol: str                  # 例如：'000001'（平安银行）
    start_date: str = "19900101" # YYYYMMDD
    end_date: str = "20991231"   # YYYYMMDD
    adjust: Adjust = ""          # '', 'qfq', 'hfq'


def _yyyymmdd(s: str) -> str:
    # 允许传入 YYYY-MM-DD / YYYYMMDD
    s = s.strip()
    if "-" in s:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%Y%m%d")
    if len(s) == 8 and s.isdigit():
        return s
    raise ValueError(f"日期格式错误：{s}，请用 YYYYMMDD 或 YYYY-MM-DD")


def get_a_stock_daily(params: DailyKlineParams) -> pd.DataFrame:
    """
    获取A股个股历史日线（东方财富数据源）
    返回列一般包含：日期/开盘/收盘/最高/最低/成交量/成交额/振幅/涨跌幅/涨跌额/换手率
    """
    print(f"获取A股日线：{params}")
    df = ak.fund_etf_hist_em(
        symbol=params.symbol,
        period="daily",
        start_date=_yyyymmdd(params.start_date),
        end_date=_yyyymmdd(params.end_date),
        adjust=params.adjust,
    )
    print(df.columns)
    # 兼容性：将“日期”转为 datetime，按日期升序
    if "日期" in df.columns:
        df["日期"] = pd.to_datetime(df["日期"])
        df = df.sort_values("日期").reset_index(drop=True)
    return df


def get_a_stock_spot() -> pd.DataFrame:
    """
    获取A股全市场实时行情快照（包含代码/名称/最新价/涨跌幅等）
    """
    df = ak.stock_zh_a_spot_em()
    return df


def get_index_daily(index_code: str, start_date: str = "19900101", end_date: str = "20991231") -> pd.DataFrame:
    """
    获取A股指数日线（如：'000300' 沪深300，'000001' 上证指数）
    """
    df = ak.stock_zh_index_daily_em(symbol=index_code)
    # stock_zh_index_daily_em 通常返回 date/open/close/high/low/volume/amount
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df[(df["date"] >= pd.to_datetime(_yyyymmdd(start_date)))
                & (df["date"] <= pd.to_datetime(_yyyymmdd(end_date)))]
        df = df.sort_values("date").reset_index(drop=True)
    return df

def get_concept_board_spot() -> pd.DataFrame:
    """
    获取概念板块行情快照（东方财富）
    常见字段：板块名称、涨跌幅、领涨股、成交额等（以实际返回为准）
    """
    return ak.stock_board_concept_name_em()


def get_concept_board_members(board_name: str) -> pd.DataFrame:
    """
    获取概念板块成分股（东方财富）
    board_name: 概念板块名称（如 '人工智能'、'ChatGPT' 等，以列表接口返回为准）
    """
    return ak.stock_board_concept_cons_em(symbol=board_name)

def save_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False, encoding="utf-8-sig")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="获取A股股票/指数数据（akshare）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_concept = sub.add_parser("concept", help="概念板块数据（列表/成分股）")
    p_concept.add_argument("--action", required=True, choices=["list", "members"], help="list: 概念板块列表; members: 成分股")
    p_concept.add_argument("--name", default="", help="概念板块名称（action=members 时必填）")
    p_concept.add_argument("--out", default="", help="保存为 CSV 的路径（可选）")

    p_daily = sub.add_parser("daily", help="获取个股历史日线")
    p_daily.add_argument("--symbol", required=True, help="股票代码，如 000001 / 600519")
    p_daily.add_argument("--start", default="19900101", help="开始日期 YYYYMMDD 或 YYYY-MM-DD")
    p_daily.add_argument("--end", default="20991231", help="结束日期 YYYYMMDD 或 YYYY-MM-DD")
    p_daily.add_argument("--adjust", default="", choices=["", "qfq", "hfq"], help="复权：''/qfq/hfq")
    p_daily.add_argument("--out", default="", help="保存为 CSV 的路径（可选）")

    p_spot = sub.add_parser("spot", help="获取A股实时行情")
    p_spot.add_argument("--out", default="", help="保存为 CSV 的路径（可选）")

    p_index = sub.add_parser("index", help="获取指数日线")
    p_index.add_argument("--code", required=True, help="指数代码，如 000300 / 000001")
    p_index.add_argument("--start", default="19900101", help="开始日期 YYYYMMDD 或 YYYY-MM-DD")
    p_index.add_argument("--end", default="20991231", help="结束日期 YYYYMMDD 或 YYYY-MM-DD")
    p_index.add_argument("--out", default="", help="保存为 CSV 的路径（可选）")

    args = parser.parse_args(argv)

    if args.cmd == "daily":
        df = get_a_stock_daily(
            DailyKlineParams(
                symbol=args.symbol,
                start_date=args.start,
                end_date=args.end,
                adjust=args.adjust,
            )
        )
    elif args.cmd == "spot":
        df = get_a_stock_spot()
    elif args.cmd == "index":
        df = get_index_daily(args.code, args.start, args.end)
    elif args.cmd == "concept":
        if args.action == "list":
            df = get_concept_board_spot()
        elif args.action == "members":
            if not args.name.strip():
                raise SystemExit("concept members 需要 --name 概念板块名称（先用 concept --action list 查看）")
            df = get_concept_board_members(args.name.strip())
        else:
            raise SystemExit("未知 concept action")
    else:
        raise SystemExit("未知命令")

    # 默认打印前几行和行数
    print(df.head(10).to_string(index=False))
    print(f"\nrows={len(df)}, cols={len(df.columns)}")

    if getattr(args, "out", ""):
        save_csv(df, args.out)
        print(f"saved: {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())