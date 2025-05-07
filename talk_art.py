import sqlite3
import pymysql
import argparse
import random
parser = argparse.ArgumentParser()

parser.add_argument("--mode", type=str, default="accurate")
parser.add_argument("--key", type=str, default="")
parser.add_argument("--sub", type=str, default="0,")
parser.add_argument("--type", type=str, default="menu,talk,nothings,rand_nothings")
parser.add_argument("--menu", type=str, default="")
args = parser.parse_args()

# 打开数据库连接
db = pymysql.connect(host="localhost", user="root", password="1234", database="SweetNothings")
# db = sqlite3.connect('SweetNothings.db')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

def initialize_database():
    """初始化数据库表结构"""


    # 创建对话表
    cursor.execute("""CREATE TABLE IF NOT EXISTS talk_art(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pasterCatName TEXT,
        title TEXT,
        content TEXT)""")
    
    # 创建情话表
    cursor.execute("""CREATE TABLE IF NOT EXISTS nothings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sentence TEXT)""")
    
    db.commit()

# initialize_database()  # 确保表存在

def main():

    menu = args.type.split(",")
    if "talk" in menu:
        query_talk()
    if "nothings" in menu:
        nothings()
    if "rand_nothings" in menu:
        rand_nothings()
    if "menu" in menu:
        query_menu()


    # 关闭数据库连接
    cursor.close()
    db.close()

def menu():
    query_sql = """select pasterCatName from talk_art GROUP BY pasterCatName;"""
    cursor.execute(query_sql)
    return cursor.fetchall()
pasterCatName = menu()

def query_menu():
    print("\n\033[1;31m菜单:\033[0m")
    for index in range(len(pasterCatName)):
        print(index+1,".",pasterCatName[index][0],end="\t\t\t\t")
    print("\n")

def query_talk():


    try:
        paster = int(args.menu)
    except:
        paster = ""
    try:
        kclass = pasterCatName[paster-1][0]
    except:
        kclass = ""

    if args.mode == "fuzzy":
        query_sql = """select * from talk_art where pasterCatName like '%%%s%%' and title like '%%%s%%' or content like '%%%s%%'"""%(kclass,args.key,args.key)
        #print(query_sql)
    elif args.mode == "accurate":
        query_sql = """select * from talk_art where pasterCatName like '%%%s%%' and title like '%%%s%%' """%(kclass,args.key)
        #print(query_sql)
    cursor.execute(query_sql)
    res = cursor.fetchall()
    length = len(res)
    try:
        start,end = [int(i) for i in args.sub.split(",")]
    except:
        start = 0
        end = length


    try:
        if end >= length:
            end = length
    except:
        end = length
    print("\033[1;31;m对话:\033[0m")

    for index in range(start,end):
        print(index + 1,"*"*50)
        print("\033[1;32m%s\033[0m"%res[index][1])
        print("\033[1;34m%s\033[0m"%res[index][2])
        print(res[index][3])
    print("总数:",len(res))

def nothings():
    try:
        keyword = args.key
    except:
        keyword = ""
    query_sql = """select sentence from nothings where sentence like '%%%s%%'"""%(keyword)
    cursor.execute(query_sql)
    res = cursor.fetchall()
    length = len(res)
    try:
        start,end = [int(i) for i in args.sub.split(",")]
    except:
        start = 0
        end = length


    try:
        if end >= length:
            end = length
    except:
        end = length
    print("\n\033[1;31;m土味情话:\033[0m")


    try:
        for index in range(start,end):
            print(index+1,"*"*50)
            print("\033[1;33m%s\033[0m"%res[index][0])
        print("总数:",index+1)
    except:
        pass

def rand_nothings():
    query_sql = """select sentence from nothings ORDER BY RAND() LIMIT 20"""
    cursor.execute(query_sql)
    res = cursor.fetchall()
    # 定义可用的颜色代码 (ANSI颜色代码)
    colors = [
        '\033[31m',  # 红色
        '\033[32m',  # 绿色
        '\033[33m',  # 黄色
        '\033[34m',  # 蓝色
        '\033[35m',  # 紫色
        '\033[36m',  # 青色
        '\033[91m',  # 亮红
        '\033[92m',  # 亮绿
        '\033[93m',  # 亮黄
        '\033[94m',  # 亮蓝
        '\033[95m',  # 亮紫
        '\033[96m',  # 亮青
    ]

    reset_color = '\033[0m'  # 重置颜色

    for count, (sentence,) in enumerate(res, start=1):
        # 随机选择一种颜色
        color = random.choice(colors)
        print(f"{count}. {color}{sentence.replace("<br>","\n")}{reset_color}")


if __name__ == '__main__':
    main()
    # rand_nothings()



