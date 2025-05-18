import sqlite3
import pymysql
import argparse
import random
from abc import ABC, abstractmethod


# 抽象工厂基类
class DatabaseHandler(ABC):
    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def execute_query(self, sql):
        pass

    @abstractmethod
    def close(self):
        pass

    @property
    @abstractmethod
    def random_func(self):
        pass


# MySQL 具体实现
class MySQLHandler(DatabaseHandler):
    def __init__(self):
        self.connection = None
        self.cursor = None
        self._random_func = "RAND()"

    @property
    def random_func(self):
        return self._random_func

    def connect(self, **kwargs):
        self.connection = pymysql.connect(
            host=kwargs.get('host'),
            user=kwargs.get('user'),
            password=kwargs.get('password'),
            database=kwargs.get('database')
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


# SQLite 具体实现
class SQLiteHandler(DatabaseHandler):
    def __init__(self):
        self.connection = None
        self.cursor = None
        self._random_func = "RANDOM()"

    @property
    def random_func(self):
        return self._random_func

    def connect(self, **kwargs):
        self.connection = sqlite3.connect(kwargs.get('database'))
        self.cursor = self.connection.cursor()

    def execute_query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


# 数据库工厂
class DBFactory:
    @staticmethod
    def create_handler(db_type):
        handlers = {
            'mysql': MySQLHandler,
            'sqlite': SQLiteHandler
        }
        return handlers[db_type]()


# 参数解析
# parser = argparse.ArgumentParser()
# parser.add_argument("--mode", type=str, default="accurate")
# parser.add_argument("--key", type=str, default="")
# parser.add_argument("--sub", type=str, default="0,")
# parser.add_argument("--type", type=str, default="menu,talk,nothings,rand_nothings")
# parser.add_argument("--menu", type=str, default="")
# parser.add_argument("--db-type", choices=['mysql', 'sqlite'], default='sqlite')
# parser.add_argument("--db-name", default='SweetNothings.db')
# parser.add_argument("--host", default='localhost')
# parser.add_argument("--user", default='root')
# parser.add_argument("--password", default='')
# args = parser.parse_args()
#
# # 初始化数据库连接
# db_handler = DBFactory.create_handler(args.db_type)
# connection_params = {
#     'database': args.db_name,
#     'host': args.host,
#     'user': args.user,
#     'password': args.password
# }
# db_handler.connect(**connection_params)


class SweetNothings:
    def __init__(self, handler, args):
        self.db = handler
        self.args = args
        self.paster_cat_names = self._get_menu_data()

    def _get_menu_data(self):
        sql = """SELECT pasterCatName FROM talk_art GROUP BY pasterCatName"""
        return [row[0] for row in self.db.execute_query(sql)]

    def query_menu(self):
        print("\n\033[1;31m菜单:\033[0m")
        for idx, name in enumerate(self.paster_cat_names, 1):
            print(f"{idx}. {name}", end="\t\t")
        print("\n")

    def query_talk(self):

        sql = f"""SELECT * FROM talk_art 
                    WHERE pasterCatName LIKE '%{self.args.key}%' OR title LIKE  '%{self.args.key}%'  OR content LIKE  '%{self.args.key}%' """

        results = self.db.execute_query(sql)
        self._display_results(results, "对话")

    def nothings(self):
        sql = f"""SELECT sentence FROM nothings 
                WHERE sentence LIKE '%%{self.args.key}%%'"""
        results = self.db.execute_query(sql)
        self._display_results(results, "土味情话")

    def rand_nothings(self):
        sql = f"""SELECT sentence FROM nothings 
                ORDER BY {self.db.random_func} LIMIT 20"""
        results = self.db.execute_query(sql)
        self._display_colored_results(results)

    def _display_results(self, results, title):
        print(f"\033[1;31m{title}:\033[0m")

        for idx in range(len(results)-1):
            row = results[idx]
            print(f"{idx + 1} {'*' * 50}")
            print(f"\033[1;34m{row[1]}\033[0m".replace(self.args.key,f"\033[1;31m{self.args.key}\033[0m").replace("\\n","\n"))
            print(row[2].replace(self.args.key,f"\033[1;31m{self.args.key}\033[0m").replace("\\n","\n"))
            print(f"\033[1;33m{row[3]}\033[0m".replace(self.args.key,f"\033[1;31m{self.args.key}\033[0m").replace("\\n","\n"))
        print(f"总数: {len(results)}")

    def _display_colored_results(self, results):
        colors = ['\033[3{}m'.format(i) for i in range(1, 7)]
        reset = '\033[0m'

        for idx, row in enumerate(results, 1):
            color = random.choice(colors)
            sentence = row[0].replace("<br>", "\n")
            print(f"{idx}. {color}{sentence}{reset}")


# 命令行参数解析
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", default="")
    parser.add_argument("--type", default="menu,talk,nothings,rand_nothings")
    parser.add_argument("--menu", default="")
    parser.add_argument("--db-type", choices=['mysql', 'sqlite'], default='sqlite')
    parser.add_argument("--db-name", default='/Users/ivan/Desktop/project/mac-tools/SweetNothings.db')
    parser.add_argument("--host", default='localhost')
    parser.add_argument("--user", default='root')
    parser.add_argument("--password", default='')
    return parser.parse_args()


def main():
    args = parse_args()

    db_handler = DBFactory.create_handler(args.db_type)
    db_handler.connect(
        database=args.db_name,
        host=args.host,
        user=args.user,
        password=args.password
    )

    app = SweetNothings(db_handler, args)

    for func_type in args.type.split(','):
        if func_type == 'menu':
            app.query_menu()
        elif func_type == 'talk':
            app.query_talk()
        elif func_type == 'nothings':
            app.nothings()
        elif func_type == 'rand_nothings':
            app.rand_nothings()

    db_handler.close()


if __name__ == '__main__':
    main()
