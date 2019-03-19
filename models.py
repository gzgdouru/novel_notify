from datetime import datetime

import peewee_async
import peewee

from settings import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_CHARSET

_database = peewee_async.MySQLDatabase(DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
                                       charset=DB_CHARSET)
objects = peewee_async.Manager(_database)
_database.set_allow_sync(False)


class NovelNotify(peewee.Model):
    name = peewee.CharField(verbose_name="小说名称")
    chapter_name = peewee.CharField(verbose_name="章节名称")
    add_time = peewee.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        database = _database
        table_name = "tb_novel_notify"
