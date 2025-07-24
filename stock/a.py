# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('203b222725198c51a5a9b17ae03cfe7418089999d1b7874a1b1cf400')

# 拉取数据
df = pro.rt_k(**{
    "topic": "",
    "ts_code": 2401,
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "name",
    "pre_close",
    "high",
    "open",
    "low",
    "close",
    "vol",
    "amount",
    "num"
])
print(df)