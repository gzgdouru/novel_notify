from datetime import datetime

import peewee_async
import peewee

from settings import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_CHARSET

_database = peewee_async.MySQLDatabase(DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
                                       charset=DB_CHARSET)
objects = peewee_async.Manager(_database)
_database.set_allow_sync(False)


class NovelModel(peewee.Model):
    name = peewee.CharField(verbose_name="小说名称", unique=True)
    add_time = peewee.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        database = _database
        table_name = "tb_novel"


class ChapterModel(peewee.Model):
    novel = peewee.ForeignKeyField(NovelModel, backref="chapters")
    name = peewee.CharField(verbose_name="章节名称")
    add_time = peewee.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        database = _database
        table_name = "tb_chapter"
        constraints = [peewee.SQL("CONSTRAINT uc_novel_name UNIQUE (novel_id,name)")]


if __name__ == "__main__":
    # async def test():
    #     novels = await objects.execute(NovelModel.select())
    #     for novel in novels:
    #         print(novel)
    #
    #
    # import asyncio
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test())
    # print("end...")

    _database.create_tables([NovelModel, ChapterModel])
