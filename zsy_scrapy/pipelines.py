# -*- coding: utf-8 -*-
import MySQLdb.cursors
import MySQLdb
from twisted.enterprise import adbapi
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ZsyScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


# 异步连接数据库
class MysqlTiPipeline(object):
    # 初始化
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 使用setting配置文件的值
    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DB"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        # 列表传递值
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    # 重载方法
    def process_item(self, item, spider):
        # 异步提交
        self.dbpool.runInteraction(self.insert_sql, item)

    # 插入sql的具体方法
    def insert_sql(self, cursor, item):
        if self.select_sql(cursor, item) == 0:
            insert_sql = """
                insert into jrgz(id, title, content, source, create_time, visits, url, md5_url, state)
                values(REPLACE(UUID(),"-",""), %s, %s, null, null, null, %s, %s, null)
            """
            # 执行SQL语句
            cursor.execute(insert_sql, ((str(item["title"])).encode("utf8"), (str(item["content"])).encode("utf8")
                                        , (str(item["url"])).encode("utf8"), (str(item["md5_url"])).encode("utf8")))

    def select_sql(self, cursor, item):
        select_sql = """
            select md5_url from jrgz WHERE md5_url=%s
        """
        # 执行SQL语句
        return cursor.execute(select_sql, ((str(item["md5_url"])).encode("utf8")))
