#-*- coding:utf-8 -*-
'''
Created on 2019年2月14日
@author: zhilh
Description: 数据库连接封装
'''
import psycopg2
import pymysql
import pymssql
import cx_Oracle
from framework.readConfig import ReadConfig


cf=ReadConfig()
DATABASE_PARA = {'sql_name': cf.get_config('234_DATABASE', 'dbtype'),
            'database': cf.get_config('234_DATABASE', 'dbname'),
            'user': cf.get_config('234_DATABASE', 'dbuser'),
            'password': cf.get_config('234_DATABASE', 'dbpassword'),
            'port': cf.get_config('234_DATABASE', 'dbport'),
            'host': cf.get_config('234_DATABASE', 'dbhost'),
           'charset': cf.get_config('234_DATABASE', 'dbcharset'),
            }

FIND_BY_ATTR = "findByAttr" # 根据条件查询一条或多条记录
FIND_BY_SQL = "findBySql" # 根据sql查找
INSERT = "insert" # 插入
UPDATE_BY_ATTR = "updateByAttr" # 更新数据
DELETE_BY_ATTR = "deleteByAttr" # 删除数据
COUNT = "count" # 统计行
COUNT_BY_SQL = "countBySql" # 自定义sql 统计影响行数
EXIST = "exist" # 是否存在该记录


class DBUtil:
    #初始化连接参数
    def __init__(self,kwargs=DATABASE_PARA):
        if kwargs.get("sql_name"):
            self.sql_name = kwargs.get("sql_name")
        if kwargs.get("database"):
            self.database = kwargs.get("database")
        if kwargs.get("user"):
            self.user = kwargs.get("user")
        if kwargs.get("password"):
            self.password = kwargs.get("password")
        if kwargs.get("port"):
            self.port = kwargs.get("port")
        if kwargs.get("host"):
            self.host = kwargs.get("host")
        if kwargs.get("charset"):
            self.charset = kwargs.get("charset")
        if not (self.sql_name and self.host and self.port and self.user and self.password and self.database):
            raise Warning("missing some params!")
        self.sql_conn = {'mysql': pymysql,
                    'postgresql': psycopg2,
                    'sqlserver': pymssql,
                    'orcle': cx_Oracle
                    }
        self._conn,self._cursor = self.connect_db()  
       
    def connect_db(self):
        '''创建连接、游标'''
        conn = False
        try:
            conn  = self.sql_conn[self.sql_name].connect(host=self.host,
                                                        port=self.port,
                                                        user=self.user,
                                                        password=self.password,
                                                        database=self.database,
                                                        #charset=self.charset,
                                                        )
            cursor = conn.cursor()
        except Exception as data:
            conn = False
            cursor = False
            raise NameError("connect database failed, %s" % data)
        return conn,cursor

    def close_db(self):
        """关闭游标和数据库连接"""
        if(self._conn is not None):
            try:
                if(type(self._cursor)=='object'):
                    self._cursor.close()
                if(type(self._conn)=='object'):
                    self._conn.close()
            except Exception as data:
                raise NameError("close database exception, %s,%s,%s" % (data, type(self._cursor), type(self._conn)))
        
    def test_conn(self):
        '''测试连接'''
        #print(self._conn)
        if self._conn:
            print("conn success!")
        else:
            print('conn error!')    
            
    def __getCursor(self):
        """获取游标"""
        if self._cursor is None:
            self._cursor = self._conn.cursor()
        return self._cursor
    
    def __del__(self):
        self.close_db()

    def execSql(self,sql):
        '''无拼接sql, 慎用, 容易sql注入'''
        cursor = self.__getCursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()# fetchone是一条记录， fetchall 所有记录
            self._conn.commit()#提交到数据库执行
        except Exception as msg:
            self._conn.rollback()#如果发生错误则回滚
            print(msg)
            return False
        return data

    # def findBySql(self, sql, params={}, limit=0, join='AND'):
    def findBySql(self, **kwargs):
        """
        根据自定义sql语句查询记录
        sql: 拼接好的sql查询语句
        limit:0表示所有记录
        join：AND|OR.不传取AND
        params = dict(field=value),条件参数
        """
        cursor = self.__getCursor()
        # sql = self.__joinWhere(kwargs["sql"], kwargs["params"], kwargs["join"])
        if kwargs.get("join", 0) == 0: kwargs["join"] = "AND"
        sql = self.__joinWhere(**kwargs)
        sql = sql%(tuple(kwargs["params"].values()))
        #print(sql)
        cursor.execute(sql)
        rows = cursor.fetchmany(size=kwargs["limit"]) if kwargs["limit"] > 0 else cursor.fetchall()# fetchone是一条记录， fetchall 所有记录
        coloumns = [row[0] for row in cursor.description]
        result = [dict(zip(coloumns,row)) for row in rows] if rows else None
        return result

    # def count(self,table,params={},join='AND'):
    def count(self, **kwargs):
        """根据条件统计行数
        table: 表名
        不传params参数，就是查找全部.
        join = 'AND | OR' 默认AND;        
        """
        if kwargs.get("join", 0) == 0: kwargs["join"] = "AND"
        sql = 'SELECT COUNT(*) FROM "%s"' % kwargs["table"]
        # sql = self.__joinWhere(sql, kwargs["params"], kwargs["join"])
        kwargs["sql"] = sql
        sql = self.__joinWhere(**kwargs)
        cursor = self.__getCursor()
        sql=sql%(tuple(kwargs["params"].values()))
        #print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0] if result else 0
    
    # def countBySql(self,sql,params = {},join = 'AND'):
    def countBySql(self, **kwargs):
        """自定义sql 统计影响行数
        sql: 拼接好的sql查询语句
        join：AND|OR.不传取AND
        params = dict(field=value),条件参数
        """
        if kwargs.get("join", 0) == 0: kwargs["join"] = "AND"
        cursor = self.__getCursor()
        # sql = self.__joinWhere(kwargs["sql"], kwargs["params"], kwargs["join"])
        sql = self.__joinWhere(**kwargs)
        sql = sql%(tuple(kwargs["params"].values()))
        #print(sql)
        cursor.execute(sql)
        result = cursor.fetchone() # fetchone是一条记录， fetchall 所有记录
        return result[0] if result else 0

    # def insert(self,table,data):
    def insert(self, **kwargs):
        """新增一条记录
          table: 表名
          data: dict 插入的数据
        """
        fields = ','.join('"'+k+'"' for k in kwargs["data"].keys())
        values = ','.join(("%s", ) * len(kwargs["data"]))
        sql = 'INSERT INTO "%s" (%s) VALUES (%s)' % (kwargs["table"], fields, values)
        cursor = self.__getCursor()
        sql = sql%(tuple(kwargs["data"].values()))
        #print(sql)
        #cursor.execute(sql)
        #insert_id = cursor.lastrowid
        #self._conn.commit()
        #return insert_id
        #更新数据库需要做事务处理
        try:
            cursor.execute(sql)
            self._conn.commit()
            data = cursor.lastrowid
            return data
        except Exception as msg:
            self._conn.rollback()
            print(msg)
            return False

    # def updateByAttr(self,table,data,params={},join='AND'):
    def updateByAttr(self, **kwargs):
        """
        更新数据
        table: 表名
        data: dict 更新的数据
        params = dict(field=value) 条件参数
        join = 'AND | OR'，默认AND
        """
        if kwargs.get("params", 0) == 0:
            kwargs["params"] = {}
        if kwargs.get("join", 0) == 0:
            kwargs["join"] = "AND"
        fields = ','.join('"' + k + '"=%s' for k in kwargs["data"].keys())
        values = list(kwargs["data"].values())
        values.extend(list(kwargs["params"].values()))
        sql = "UPDATE %s SET %s " % (kwargs["table"], fields)
        kwargs["sql"] = sql
        sql = self.__joinWhere(**kwargs)
        cursor = self.__getCursor()
        sql = sql%(tuple(values))
        #print(sql)
        #cursor.execute(sql)
        #self._conn.commit()
        #return cursor.rowcount
        #更新数据库需要做事务处理
        try:
            cursor.execute(sql)
            self._conn.commit()
            data = cursor.rowcount
            return data
        except Exception as msg:
            self._conn.rollback()
            print(msg)
            self._conn.rollback()
            return False

    # def deleteByAttr(self,table,params={},join='AND'):
    def deleteByAttr(self, **kwargs):
        """删除数据
        table: 表名
        params: 条件参数 ,不传params参数，就是删除全部    
        join = 'AND | OR'，默认AND    
        """
        if kwargs.get("params", 0) == 0:
            kwargs["params"] = {}
        if kwargs.get("join", 0) == 0:
            kwargs["join"] = "AND"
        # fields = ','.join('"'+k+'"=%s' for k in kwargs["params"].keys())
        sql = "DELETE FROM %s " % kwargs["table"]
        kwargs["sql"] = sql
        # sql = self.__joinWhere(sql, kwargs["params"], kwargs["join"])
        sql = self.__joinWhere(**kwargs)
        cursor = self.__getCursor()
        sql = sql%(tuple(kwargs["params"].values()))
        #print(sql)
        #cursor.execute(sql)
        #self._conn.commit()
        #return cursor.rowcount
        #更新数据库需要做事务处理
        try:
            cursor.execute(sql)
            self._conn.commit()
            data = cursor.rowcount
            return data
        except Exception as msg:
            self._conn.rollback()
            print(msg)
            self._conn.rollback()
            return False

    # def exist(self,table,params={},join='AND'):
    def exist(self, **kwargs):
        """判断是否存在
        table: 表名
        不传params参数，就是查找全部.
        join = 'AND | OR' 默认AND;
        """        
        return self.count(**kwargs) > 0

    # def __joinWhere(self,sql,params,join):
    def __joinWhere(self, **kwargs):
        """转换params为where连接语句"""
        if kwargs["params"]:
            keys,_keys = self.__tParams(**kwargs)
            where = ' AND '.join(k+'='+_k for k,_k in zip(keys,_keys)) if kwargs["join"] == 'AND' else ' OR '.join(k+'='+_k for k,_k in zip(keys,_keys))
            kwargs["sql"]+=' WHERE ' + where
        return kwargs["sql"]

    # def __tParams(self,params):
    def __tParams(self, **kwargs):
        keys = ['"'+k+'"' for k in kwargs["params"].keys()]
        _keys = ['%s' for k in kwargs["params"].keys()]
        return keys,_keys

    # def __query(self,table,criteria={},whole=False):
    def findByAttr(self, **kwargs):
        '''根据条件查询记录
        table: 表名
        criteria: dict，criteria里面可以传select,where,group by,having,order by,limt,offset
        whole=True 查询返回所有记录，whole=False 查询返回第一条记录
        '''
        if kwargs.get("whole", False) == False or kwargs["whole"] is not True:
            kwargs["whole"] = False
            kwargs["criteria"]['limit'] = 1
        # sql = self.__contact_sql(kwargs["table"], kwargs["criteria"])
        sql = self.__contact_sql(**kwargs)
        cursor = self.__getCursor()
        #print(sql)
        cursor.execute(sql)
        coloumns = [row[0] for row in cursor.description]
        rows = cursor.fetchall() if kwargs["whole"] else cursor.fetchone()
        result = [dict(zip(coloumns, row)) for row in rows] if kwargs["whole"] else dict(zip(coloumns, rows)) if rows else None
        return result

    # def __contact_sql(self,table,criteria):
    def __contact_sql(self, **kwargs):
        sql = 'SELECT '
        if kwargs["criteria"] and type(kwargs["criteria"]) is dict:
            #select fields
            if 'select' in kwargs["criteria"]:
                fields = kwargs["criteria"]['select'].split(',')
                sql+= ','.join('"'+field+'"' for field in fields)
            else:
                sql+=' * '
            #table
            sql+=' FROM "%s"'% kwargs["table"]
            #where
            if 'where' in kwargs["criteria"]:
                sql+=' WHERE '+ kwargs["criteria"]['where']
            #group by
            if 'group' in kwargs["criteria"]:
                sql+=' GROUP BY '+ kwargs["criteria"]['group']
            #having
            if 'having' in kwargs["criteria"]:
                sql+=' HAVING '+ kwargs["criteria"]['having']
            #order by
            if 'order' in kwargs["criteria"]:
                sql+=' ORDER BY '+ kwargs["criteria"]['order']
            #limit
            if 'limit' in kwargs["criteria"]:
                sql+=' LIMIT '+ str(kwargs["criteria"]['limit'])
            #offset
            if 'offset' in kwargs["criteria"]:
                sql+=' OFFSET '+ str(kwargs["criteria"]['offset'])
        else:
            sql+=' * FROM "%s"'% kwargs["table"]
        return sql
    
    def findKeySql(self, key ,**kwargs):
        sqlOperate = {
        COUNT: lambda: self.count(**kwargs),
        COUNT_BY_SQL: lambda: self.countBySql(**kwargs),
        INSERT: lambda: self.insert(**kwargs),
        UPDATE_BY_ATTR: lambda: self.updateByAttr(**kwargs),
        DELETE_BY_ATTR: lambda: self.deleteByAttr(**kwargs),
        EXIST: lambda: self.exist(**kwargs),
        FIND_BY_ATTR: lambda: self.findByAttr(**kwargs),
        FIND_BY_SQL: lambda: self.findBySql(**kwargs)

        }
        return sqlOperate[key]()

def testDB():
    db = DBUtil()
    db.test_conn()
    
    #插入数据
    print(db.findKeySql(INSERT, table="user_info", data={"name":"'王明'", "phone": "'13901139001'","id_card": "'510100198609012527'","address": "'成都武侯区'"}))
    print(db.insert(table="user_info", data={"id":"11","name":"'陈家人'", "phone": "'1390113991'","id_card": "'515405198609012527'","address": "'成都双流区'"}))
    
    # 根据字段更新数据库中的记录，join可以传AND,OR,不传默认取AND
    print(db.findKeySql(UPDATE_BY_ATTR, table="user_info",data={"name": "'李si'"}, params={"name": "'li四'"}, join='AND'))
    print(db.updateByAttr(table="user_info",data={"name": "'赵宽永'","id_card": "'512301198609012445'"}, params={"name": "'李si'","id":"61"}, join='AND'))
    
    #根据字段删除,不传params参数，就是删除全部
    print(db.findKeySql(DELETE_BY_ATTR, table="user_info", params={"name": "'123'"}))
    print(db.deleteByAttr(table="user_info", params={"id": "61"}))
    
    #根据字段查找多条记录，whole不传就查一条记录，criteria里面可以传select,where,group by,having,order by,limt,offset
    print(db.findKeySql(FIND_BY_ATTR, table="user_info", criteria= {"where": "phone like '%1380%'"}, whole=True))
    print(db.findKeySql(FIND_BY_ATTR, table="user_info", criteria= {"select": 'name,phone',"where": "phone like '%1380%'"}, whole=True))
    print(db.findByAttr(table="user_info", criteria= {"where": "phone like '%1380%'"}, whole=True))
    
    # 根据字段查一条记录，和上面的查多条记录参数基本一样，少了个whole参数
    print(db.findKeySql(FIND_BY_ATTR, table="user_info", criteria= {"where": "address='成都高新区'"}))
    print(db.findByAttr(table="user_info", criteria= {"select": 'name,phone',"where": "phone like '%1380%'"}, whole=False))
    
    # 根据自定义sql语句查询记录，limit:0表示所有记录，join：AND|OR.不传取AND
    print(db.findKeySql(FIND_BY_SQL, sql="select * from user_info ", params={"name": "'张san'"}, limit=0))
    print(db.findBySql(sql="select *  from user_info where id > 1 order by name",params={}, limit=3))
    
    # 查找是否存在该记录,不传params参数，就是查找全部.join同上;
    print(db.findKeySql(EXIST, table="user_info", params={"name": "'张san'"},join='AND'))
    print(db.exist(table="user_info", params={"name": "'王小明'"},join='AND'))
    
    #自定义sql语句统计count
    print(db.findKeySql(COUNT_BY_SQL, sql='select count(*) from "user_info"', params={"address": "'成都高新区'","address": "'成都高新区'"}, join="AND"))
    print(db.countBySql(sql="select count(*) from user_info where id >5", params={}))

    # 根据字段统计count, join>>AND,OR,可以不传，默认为AND
    print(db.findKeySql(COUNT, table="user_info", params={"address": "'成都高新区'","address": "'成都高新区'"}, join="OR"))
    print(db.count(table="user_info", params={}))
    
    #无拼接sql，慎用，容易sql注入
    print(db.execSql('select * from user_info'))

if __name__ == "__main__":
    #testDB()
    pass
    


    