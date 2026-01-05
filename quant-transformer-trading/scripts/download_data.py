import argparse
import pandas as pd
import yfinance as yf

def download_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    下载股票数据
    :param symbol: 股票代码
    :param start: 开始日期 (YYYY-MM-DD)
    :param end: 结束日期 (YYYY-MM-DD)
    :return: 股票数据的 DataFrame
    """
    df = yf.download(symbol, start=start, end=end)
    return df

def main():
    parser = argparse.ArgumentParser(description="下载股票数据")
    parser.add_argument("--symbol", required=True, help="股票代码，如 AAPL")
    parser.add_argument("--start", required=True, help="开始日期 YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="结束日期 YYYY-MM-DD")
    parser.add_argument("--output", default="data.csv", help="输出文件名")
    
    args = parser.parse_args()
    
    data = download_data(args.symbol, args.start, args.end)
    data.to_csv(args.output)
    print(f"数据已保存到 {args.output}")

if __name__ == "__main__":
    main()