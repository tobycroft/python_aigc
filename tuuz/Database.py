import configparser

import pymysql
from pymysql import Connection

import config.db


#   1、实例化类 sql = Db()
#   参数类：
#   table方法：入参：表名
#       使用方法: sql.table('test') 或 sql.name('test')
#   where方法：可多次调用，入参：字符串或字典(key:字段名,val:值,type:对应关系,默认为'=')或数组
#       使用方法: sql.where('id=1')
#       使用方法: sql.where({'id',1})
#       使用方法: sql.where({'id',1,'<>'})
#       使用方法: sql.where({'id','(1,2)','in'})
#       使用方法: sql.where([{'id','(1,2)','in'},{'name','%我%','like'}])
#   whereRow方法:可多次调用，入参：字段名,值,对应关系
#       使用方法: sql.whereRow('id',1)
#       使用方法: sql.whereRow('id',1,'>')
#   whereIn方法:可多次调用，入参：字段名,值(逗号拼接的字符串或元组)
#       使用方法: sql.whereIn('id','1,2')
#       使用方法: sql.whereIn('id',(1,2))
#   whereLike方法:可多次调用，入参：字段名,值
#       使用方法: sql.whereLike('name','%我%')
#   alias方法:对 table 方法的表名设置 别名
#       使用方法: sql.table('test').alias('a')
#   limit方法：查询前N条数据，入参：数量
#       使用方法: sql.limit(10)
#   order方法：排序，入参：排序字符串
#       使用方法: sql.order('id desc')
#   group方法:分组，入参：字符串
#       使用方法: sql.group('name,title')
#   field方法：查询字段,入参：字符串
#       使用方法: sql.field('id,name,title,create_time')
#   distinct方法：去重，入参：True或False，默认为True
#       使用方法: sql.distinct()
#   having方法：入参：字符串
#       使用方法: sql.having('b.id=1')
# =====================================================================================
#   操作类：
#   buildSql    返回select查询语句，出参：字符串
#       使用方法: sql.buildSql()
#   find    返回符合条件的第一条数据，出参：字典
#       使用方法: sql.find()
#   count   返回符合条件的数量：出参：Int
#       使用方法: sql.count()
#   value   入参：字段名，返回符合条件的一个字段的值，出参：值
#       使用方法: sql.value('name')
#   select  返回符合条件的多数据，出参：数组<字典>
#       使用方法: sql.select()
#   get 入参：值，识别主键返回符合条件的第一条数据，出参：字典
#       使用方法: sql.get(2)
#   insert  入参：字典,字段识别后根据键名插入数据,自动剔除表中没有的字段，出参：变更数量
#       使用方法: sql.insert({'id':1,'name':'你好'})
#   insertGetId 入参：字典,字段识别后根据键名插入数据并返回自增主键值，出参：值
#       使用方法: sql.insertGetId({'id':1,'name':'你好'})
#   insertAll   入参：数组<字典>，同 insert 的数组版，出参：变更数量
#       使用方法: sql.insertAll([{'id':1,'name':'你好'}])
#   update  入参：字典，根据条件更新数据，出参：变更数量
#       使用方法: sql.update({'name':'你好'})
#   setOption 入参：字段名，变更值，根据条件更新数据，出参：变更数量
#       使用方法: sql.setOption('name','你好')
#   delete 根据条件删除数据，出参：变更数量
#       使用方法: sql.delete()
#   setInc 入参：字段名，数字(步仅值，默认为1)；字段值自增，出参：变更数量
#       使用方法: sql.setInc('num')
#       使用方法: sql.setInc('num',2)
#   setDec 入参：字段名，数字(步仅值，默认为1)；字段值自减，出参：变更数量
#       使用方法: sql.setDec('num')
#       使用方法: sql.setDec('num',2)
#   query 入参：数据库语句
#       使用方法: sql.query('delete from id=1')
#   clear 刷新传入数据
#       使用方法: sql.clear()


def format_field(val, mold):
    mold = str(mold).lower()
    if 'int' in mold:
        if val == '':
            return '0'
        return str(val)
    if 'decimal' in mold:
        if val == '':
            return '0'
        return str(val)
    if 'float' in mold:
        if val == '':
            return '0'
        return str(float(val))
    if 'double' in mold:
        if val == '':
            return '0'
        return str(float(val))
    if 'char' in mold:
        return format_val(val)
    if 'text' in mold:
        return format_val(val)
    if 'date' == mold:
        return format_val(str(val))
    if 'time' == mold:
        return format_val(str(val))
    if 'year' in mold:
        return format_val(str(val))
    if 'blob' in mold:
        return format_val(val)
    if 'datetime' == mold:
        return format_val(val)
    return format_val(val)


def format_val(val):
    types = typeof(val)
    if val is None:
        return 'null'
    if types == 'str':
        return "'%s'" % str(val).replace('\\', '').replace('\'', '"')
    if types == 'int':
        return "%s" % val
    if types == 'double':
        return "%s" % val
    return "'%s'" % str(val).replace('\\', '').replace('\'', '"')


def typeof(variate):
    mold = None
    if isinstance(variate, int):
        mold = "int"
    elif isinstance(variate, str):
        mold = "str"
    elif isinstance(variate, float):
        mold = "float"
    elif isinstance(variate, list):
        mold = "list"
    elif isinstance(variate, tuple):
        mold = "tuple"
    elif isinstance(variate, dict):
        mold = "dict"
    elif isinstance(variate, set):
        mold = "set"
    return mold


OP = {'=': '=', '>': '>', '<': '<', '>=': '>=', '<=': '<=', '<>': '<>', 'like': 'like', 'in': 'in', 'not in': '<>', 'is null': 'is null', 'is not null': 'is not null'}

conf = configparser.ConfigParser()
try:
    conf.read("conf.ini", encoding="utf-8")
    try:
        config.db.dbhost = conf.get("database", "dbhost")
    except Exception as e:
        print("数据库：读取dbhost错误:", e)
    try:
        config.db.dbuser = conf.get("database", "dbuser")
    except Exception as e:
        print("数据库：读取dbuser错误:", e)
    try:
        config.db.dbpass = conf.get("database", "dbpass")
    except Exception as e:
        print("数据库：读取dbpass错误:", e)
    try:
        config.db.dbname = conf.get("database", "dbname")
    except Exception as e:
        print("数据库：读取dbname错误:", e)
    try:
        config.db.dbport = int(conf.get("database", "dbport"))
    except Exception as e:
        print("数据库：读取dbport错误:", e)
except Exception as e:
    if "database" not in conf:
        conf["database"] = {
            "need": "False",
            "retry": "True",
            "dbhost": "127.0.0.1",
            "dbuser": "",
            "dbpass": "",
            "dbname": "",
            "dbport": 3306
        }
        with open("conf.ini", "w") as configfile:
            conf.write(configfile)
        print("e")
        exit("数据库：读取conf配置文件错误:", )


class Db(object):
    __conn: Connection = None
    __map = []
    __bindWhere = []
    __bindData = []
    __name = ''
    __column = '*'
    __alias = ''
    __join = []
    __having = []
    __distinct = False
    __option = {}
    __build = False
    __autocommit = True
    __prefix = ''
    __debug = False

    def __init__(self, conn: Connection = None, debug=False):
        if conn is not None:
            self.__autocommit = False
            self.__conn = conn
        self.__debug = debug
        self.__connect()

    def __connect(self):
        if self.__conn is None:
            if self.__debug:
                print("数据库连接至MySQL……")
            self.__conn = self.connect_to_db()
        self.cursor = self.__conn.cursor()

    def get_connection(self):
        return self.__conn

    @staticmethod
    def connect_to_db():
        return pymysql.connect(host=config.db.dbhost,
                               user=config.db.dbuser,
                               password=config.db.dbpass,
                               database=config.db.dbname,
                               port=int(config.db.dbport),
                               charset='utf8mb4',
                               connect_timeout=5,
                               init_command="SET SESSION time_zone='+08:00'",
                               autocommit=False)

    def begin(self):
        self.__autocommit = False
        self.__conn.begin()
        return self

    def commit(self):
        if self.__debug:
            print("数据库:commit", )
        self.__conn.commit()
        return self

    def rollback(self):
        if self.__debug:
            print("数据库:rollback", )
        self.__conn.rollback()
        return self

    def __close(self):
        self.cursor.close()
        self.__conn.close()

    def table(self, table):
        self.clear()
        self.__name = self.__prefix + table
        return self

    def name(self, table):
        self.clear()
        self.__name = self.__prefix + table
        return self

    def where(self, where, val_mark=None, val2=None):
        if where is not None and val_mark is not None and val2 is not None:
            return self.where({'key': where, 'val': val2, 'type': val_mark})
        elif where is not None and val_mark is not None:
            return self.where({'key': where, 'val': val_mark, 'type': '='})
        elif where is not None:
            if typeof(where) == 'dict':
                self.__map.append({'key': where.get('key'), 'val': "%s", 'type': where.get('type')})
                self.__bindWhere.append(where.get("val"))

            if typeof(where) == 'list':
                for item in where:
                    self.where(item)

            if typeof(where) == 'str':
                self.__map.append(where)
            return self
        else:
            print('禁止不使用 where 条件')
            return self

    def whereRow(self, key, val, mark='='):
        return self.where({'key': key, 'val': val, 'type': mark})

    def whereIn(self, key, val):
        if typeof(val) == 'str':
            return self.where({'key': key, 'val': tuple(str(val).split(',')), 'type': 'in'})
        return self.where({'key': key, 'val': tuple(val), 'type': 'in'})

    def whereLike(self, key, val):
        return self.where({'key': key, 'val': val, 'type': 'like'})

    def alias(self, name=''):
        self.__alias = name + ' '
        return self

    #   字段没处理明白，暂时禁用
    # def join(self, table, where, mold='inner'):
    # table = self.__prefix + table
    # self.__join.append({'table': table, 'where': where, 'mold': mold})
    # return self
    #

    def limit(self, limit=1):
        self.__option['limit'] = format_val(limit)
        return self

    def order(self, order):
        self.__option['order'] = order
        return self

    def group(self, group):
        self.__option['group'] = group
        return self

    def field(self, field):
        self.__column = field
        return self

    def distinct(self, is_true=True):
        self.__distinct = is_true
        return self

    def having(self, where):
        self.__having.append(where)
        return self

    def __comQuerySql(self):
        if self.__name is None:
            return None

        column = self.__column
        column = ['`' + element + '`' if element != '*' else element for element in column.split(',')]
        # if column == '*':
        # column = ['`' + element + '`' for element in column.split(',')]
        # for element in column.split(','):
        #     if element!='*':
        #         column = element

        sql = "select "
        if self.__distinct:
            sql += ' distinct '
        sql += str(",".join(column)) + " from `" + str(self.__name) + "`"

        if self.__alias != '':
            sql += ' ' + self.__alias

        if len(self.__join) > 0:
            if '*' in column:
                print('使用 join 必须指定字段名')
                return None
            for item in self.__join:
                sql += item['mold'] + ' join ' + item['table'] + ' on ' + item['where'] + ' '

        if len(self.__map) > 0:
            sql += ' where'
            i = 0
            for item in self.__map:
                if i > 0:
                    sql += ' and'
                i += 1
                if typeof(item) == 'str':
                    sql += ' ( `' + item + '` ) '
                elif typeof(item) == 'dict':
                    values = 'null'
                    # values = format_field(item.get('val'), column['type'])
                    values = item.get('val')
                    sql += ' ( `' + item.get('key') + '` ' + item.get('type') + ' ' + values + ' ) '

        if self.__option.get('group'):
            sql += ' group by ' + self.__option['group'] + ' '

        if len(self.__having) > 0:
            for item in self.__having:
                sql += ' ' + item

        if self.__option.get('order'):
            sql += ' order by ' + self.__option['order'] + ' '

        if self.__option.get('limit'):
            sql += ' limit ' + self.__option['limit']
        return sql

    def buildSql(self, build=True):
        # column = self.__column

        # if column == '*':
        #     column = self.__showColumn(True)
        self.__build = build
        return self

    def __getField(self, table=None):
        column = self.__column
        # if '*' in column:
        #     column = self.__showColumn(True, table=table)

        return column

    # 接下来是数据库操作

    def find(self):
        column = self.__getField()
        sql = self.__comQuerySql()
        if self.__build:
            return sql, self.__bindWhere
        if sql is None:
            return None
        result = None
        try:
            self.cursor.execute(sql, self.__bindWhere)
            result = self.cursor.fetchone()
            columns = [desc[0] for desc in self.cursor.description]
            if self.__autocommit:
                self.__close()
        except Exception as e:
            print("find-sql:", sql, self.__bindWhere)
            print(e)
            return None
        if result is None:
            return None
        data = {}
        for i, value in enumerate(result):
            data[columns[i]] = value
        return data

    def query(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchone()
            columns = [desc[0] for desc in self.cursor.description]
            if self.__autocommit:
                self.__close()
        except Exception as e:
            print("query-error:", sql, self.__bindWhere)
            print(e)
            return None
        if result is None:
            return None
        data = {}
        for i, value in enumerate(result):
            data[columns[i]] = value

    def select(self):
        if self.__name is None:
            return

        column = self.__getField()

        sql = self.__comQuerySql()
        if self.__build:
            return sql, self.__bindWhere
        if sql is None:
            return None
        result = None
        try:
            self.cursor.execute(sql, self.__bindWhere)
            result = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            if self.__autocommit:
                self.__close()
        except Exception as e:
            print(sql, self.__bindWhere)
            print(e)
            return None
        if result is None:
            return None
        data = []
        for row in result:
            row_data = {}
            for i, value in enumerate(row):
                row_data[columns[i]] = value
            data.append(row_data)
        return data

    def value(self, field):
        self.__column = field
        sql = self.__comQuerySql()
        if self.__build:
            return sql
        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if self.__autocommit:
                self.__close()
        except Exception as e:
            print(sql)
            print(e)
            return None
        if result is not None:
            return result[0]
        else:
            return None

    def count(self):
        return self.value('count(*)')

    def insert(self, data):
        fields = ''
        values = ''
        i = 0
        for key in data:
            if i == 0:
                fields = "`" + key + "`"
                # values = format_field(data[key], column['type'])
                values = '%s'
            else:
                fields += ',' + "`" + key + "`"
                # values += ',' + format_field(data[key], column['type'])
                values += ', %s '
            self.__bindData.append(data[key])
            i += 1
        if fields == '' or values == '':
            return 0
        sql = str(" insert into " + self.__name + " ( " + fields + ") values ( " + values + " ) ")
        return self.__add(sql)

    def __where_to_sql(self, sql=None):
        if sql is None:
            sql = ''
        if len(self.__map) > 0:
            sql += ' where'
            i = 0
            for item in self.__map:
                if i > 0:
                    sql += ' and'
                i += 1
                if typeof(item) == 'str':
                    sql += ' ( `' + item + '` ) '
                elif typeof(item) == 'dict':
                    sql += ' ( `' + item.get('key') + '` ' + item.get('type') + ' %s ) '
        else:
            print('禁止不使用 where 查询数据')
        return sql

    def update(self, data):
        if typeof(data) != 'dict':
            return None
        fields = ''
        sql = self.__where_to_sql()
        i = 0
        for key in data:
            if i == 0:
                fields = "`" + key + '` = %s'
            else:
                fields += str(', `' + key + '` = %s')
            self.__bindData.append(data[key])
            i += 1
        if fields == '':
            return 0
        sql = str("update " + self.__name + " set " + fields + ' ' + sql)
        return self.__edit(sql)

    def insertGetId(self, data):
        if typeof(data) != 'dict':
            return None
        fields = ''
        values = ''
        i = 0
        for key in data:
            if i == 0:
                fields = key
                # values = format_field(data[key], column['type'])
                values = "%s"
            else:
                fields += ',' + key
                # values += ',' + format_field(data[key], column['type'])
                values += ', %s'
            self.__bindData.append(data[key])
            i += 1
        if fields == '' or values == '':
            return 0
        sql = str(" INSERT INTO " + self.__name + " ( " + fields + " ) values ( " + values + " ) ")
        if self.__debug:
            print(sql, self.__bindData)
        pk = 0
        try:
            self.cursor.execute(sql, self.__bindData)
            pk = self.__conn.insert_id()
            if self.__autocommit:
                self.commit()
                self.__close()
        except Exception as e:
            if self.__autocommit:
                self.rollback()
                self.__close()
            print("insertGetId:", e)
            return None
        return pk

    # def setOption(self, key, val):
    #     return self.update({key: val})

    def insertAll(self, datas):
        if typeof(datas) != 'list':
            return None
        count = 0
        for data in datas:
            count += self.insert(data)
        return count

    def delete(self):
        i = 0
        sql = ''
        if len(self.__map) > 0:
            sql += ' where'
            for item in self.__map:
                if i > 0:
                    sql += ' and'
                i += 1
                if typeof(item) == 'str':
                    sql += ' ( ' + item + ' ) '
                elif typeof(item) == 'dict':
                    sql += ' ( ' + item.get('key') + ' ' + item.get('type') + ' ' + str(item.get('val')) + ' ) '
        else:
            print('禁止不使用 where 删除数据')
        sql = str("delete from " + self.__name + sql)
        return self.__edit(sql)

    def setInc(self, key, step=1):
        sql = self.__where_to_sql()
        fields = "`" + key + '`=`' + key + '`+%s'
        self.__bindData.append(step)
        if fields == '':
            return 0
        sql = str("update " + self.__name + " set " + fields + ' ' + sql)
        return self.__edit(sql)

    def setDec(self, key, step=1):
        sql = self.__where_to_sql()
        fields = "`" + key + '`=`' + key + '`-%s'
        self.__bindData.append(step)
        if fields == '':
            return 0
        sql = str("update " + self.__name + " set " + fields + ' ' + sql)
        return self.__edit(sql)

    def query(self, sql):
        return self.__edit(sql)

    # def __showColumn(self, is_str=False, table=None):
    #     if table is None:
    #         table = self.__name
    #     list_data = None
    #     sql = "SHOW FULL COLUMNS FROM " + table
    #     try:
    #         self.__connect()
    #         self.cursor.execute(sql)
    #         list_data = self.cursor.fetchall()
    #         self.__close()
    #         if is_str:
    #             return ','.join(list([item[0] for item in list_data]))
    #     except Exception as e:
    #         print(e)
    #     return list([{'field': item[0], 'type': item[1], 'key': item[4]} for item in list_data])

    # def __getPk(self):
    #     # fields = self.__showColumn()
    #     # for field in fields:
    #     #     if field['key'] == 'PRI':
    #     #         return field['field']
    #     return None

    def __edit(self, sql):
        if self.__debug:
            print("执行语句：", sql, self.__bindData + self.__bindWhere)
        if self.__build:
            return sql, self.__bindData + self.__bindWhere
        count = 0
        try:
            count = self.cursor.execute(sql, self.__bindData + self.__bindWhere)
            if self.__autocommit:
                self.commit()
                self.__close()
        except Exception as e:
            if self.__autocommit:
                self.rollback()
                self.__close()
            print('Database-Error:  ', sql, self.__bindData + self.__bindWhere)
            print("__edit:", e)
        return count

    def __add(self, sql):
        if self.__build:
            return sql, self.__bindData
        count = 0
        try:
            count = self.cursor.execute(sql, self.__bindData)
            if self.__autocommit:
                self.commit()
                self.__close()
        except Exception as e:
            if self.__autocommit:
                self.rollback()
                self.__close()
            print('Error:  ', sql)
            print(e)
        return count

    def clear(self):
        self.__map = []
        self.__bindWhere = []
        self.__bindData = []
        self.__name = ''
        self.__column = '*'
        self.__alias = ''
        self.__join = []
        self.__having = []
        self.__distinct = False
        self.__option = {}
