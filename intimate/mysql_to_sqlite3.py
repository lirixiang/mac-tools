import sqlite3
import pymysql
from tqdm import tqdm  # 进度条显示


class MySQLtoSQLite:
    def __init__(self, mysql_config, sqlite_db):
        self.mysql_config = mysql_config
        self.mysql_conn = pymysql.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            database=mysql_config['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        self.sqlite_conn = sqlite3.connect(sqlite_db)
        self.sqlite_cur = self.sqlite_conn.cursor()

        self.type_mapping = {
            'int': 'INTEGER',
            'tinyint': 'INTEGER',
            'smallint': 'INTEGER',
            'mediumint': 'INTEGER',
            'bigint': 'INTEGER',
            'float': 'REAL',
            'double': 'REAL',
            'decimal': 'REAL',
            'char': 'TEXT',
            'varchar': 'TEXT',
            'text': 'TEXT',
            'mediumtext': 'TEXT',
            'longtext': 'TEXT',
            'date': 'TEXT',
            'datetime': 'TEXT',
            'timestamp': 'TEXT',
            'enum': 'TEXT'
        }

    def get_mysql_tables(self):
        """更可靠的表名获取方式"""
        with self.mysql_conn.cursor() as cursor:
            # 使用INFORMATION_SCHEMA查询
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_TYPE = 'BASE TABLE'
            """, (self.mysql_config['database'],))

            # 调试输出
            tables = [row['TABLE_NAME'] for row in cursor.fetchall()]
            print(f"发现表列表: {tables}")
            return tables

    def get_table_schema(self, table_name):
        """改进的表结构转换方法"""
        with self.mysql_conn.cursor() as cursor:
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            create_sql = cursor.fetchone()['Create Table']

        # 转换关键语法
        create_sql = (
            create_sql.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
            .replace('ENGINE=InnoDB', '')
            .replace('DEFAULT CHARSET=utf8mb4', '')
            .replace('COLLATE=utf8mb4_0900_ai_ci', '')
            .replace('unsigned', '')
            .replace('`', '')  # 移除反引号
        )

        # 解析并重建字段定义
        lines = create_sql.split('\n')
        new_lines = []
        primary_key = None

        for line in lines:
            line = line.strip().strip(',').strip()
            if line.startswith('PRIMARY KEY'):
                primary_key = line.split('(')[1].split(')')[0]
                continue

            if line.startswith('CREATE TABLE'):
                new_lines.append(line)
                continue

            if line.startswith('(') or line.startswith(')'):
                continue

            # 处理字段定义
            if ' ' in line:
                field_parts = line.split()
                field_name = field_parts[0]
                field_type = field_parts[1].split('(')[0].upper()

                # 类型映射
                sqlite_type = self.type_mapping.get(field_type.lower(), 'TEXT')
                new_line = f"{field_name} {sqlite_type}"

                # 添加主键约束
                if field_name == primary_key:
                    new_line += " PRIMARY KEY AUTOINCREMENT"

                # 保留其他约束
                if 'NOT NULL' in line:
                    new_line += " NOT NULL"
                if 'DEFAULT' in line:
                    default_pos = line.find('DEFAULT')
                    new_line += ' ' + line[default_pos:]

                new_lines.append(new_line)

        # 添加结尾
        new_lines = [new_lines[0],',\n'.join(new_lines[1:])]
        new_lines.append(');')
        return '\n'.join(new_lines)

    def migrate_data(self, table_name):
        """迁移数据"""
        create_sql = self.get_table_schema(table_name)
        self.sqlite_cur.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        self.sqlite_cur.execute(create_sql)

        with self.mysql_conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{table_name}`")
            total_rows = cursor.rowcount
            columns = [col[0] for col in cursor.description]

            placeholders = ', '.join(['?'] * len(columns))
            insert_sql = f"INSERT INTO `{table_name}` VALUES ({placeholders})"

            batch_size = 1000
            with tqdm(total=total_rows, desc=f"Migrating {table_name}") as pbar:
                while True:
                    rows = cursor.fetchmany(batch_size)
                    if not rows:
                        break
                    # 转换数据格式
                    converted_rows = []
                    for row in rows:
                        converted_row = []
                        for value in row.values():
                            if isinstance(value, bytes):
                                converted_row.append(value.decode('utf-8'))
                            else:
                                converted_row.append(value)
                        converted_rows.append(tuple(converted_row))
                    self.sqlite_cur.executemany(insert_sql, converted_rows)
                    self.sqlite_conn.commit()
                    pbar.update(len(rows))

    def migrate_all(self):
        """迁移所有表"""
        tables = self.get_mysql_tables()
        print(f"发现 {len(tables)} 张表需要迁移")
        for table in tables:
            print(f"\n正在处理表: {table}")
            try:
                self.migrate_data(table)
            except Exception as e:
                print(f"迁移表 {table} 时出错: {str(e)}")
                continue

        print("\n迁移完成！")
        self.mysql_conn.close()
        self.sqlite_conn.close()


if __name__ == "__main__":
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Lirixiang520,',
        'database': 'SweerNothings'
    }

    sqlite_db = 'SweetNothings.db'

    migrator = MySQLtoSQLite(mysql_config, sqlite_db)
    migrator.migrate_all()