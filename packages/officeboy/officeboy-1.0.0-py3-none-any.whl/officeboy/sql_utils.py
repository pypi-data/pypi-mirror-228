#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/12/15 16:18
# @Author  : 江斌
# @Software: PyCharm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker
import json


def to_unicode_ascii(s):
    return json.dumps(s).replace('"', '')


def to_unicode_ascii2(s):
    return s.encode('unicode-escape').decode()


Base = declarative_base()


class Firm(Base):  # 定义映射类User，其继承上一步创建的Base
    __tablename__ = 'index_t'
    # 如果有多个类指向同一张表，那么在后边的类需要把extend_existing设为True，表示在已有列基础上进行扩展
    # 或者换句话说，sqlalchemy允许类是表的字集
    # __table_args__ = {'extend_existing': True}
    # 如果表在同一个数据库服务（datebase）的不同数据库中（schema），可使用schema参数进一步指定数据库
    # __table_args__ = {'schema': 'test_database'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    is_crawled = Column(Integer)

    def __repr__(self):
        return "<Firm(id=%s)>" % (self.id,)


class User(Base):
    __tablename__ = 'user_t'
    # 如果有多个类指向同一张表，那么在后边的类需要把extend_existing设为True，表示在已有列基础上进行扩展
    # 或者换句话说，sqlalchemy允许类是表的子集
    # __table_args__ = {'extend_existing': True}
    # 如果表在同一个数据库服务（datebase）的不同数据库中（schema），可使用schema参数进一步指定数据库
    # __table_args__ = {'schema': 'test_database'}
    __table_args__ = (
        UniqueConstraint('id', 'name', name='uix_id_name'),
        # Index('ix_id_name', 'name', 'extra'),  # 索引
        # Index('my_index', my_table.c.data, mysql_length=10) length 索引长度
        # Index('a_b_idx', my_table.c.a, my_table.c.b, mysql_length={'a': 4,'b': 9})
        # Index('my_index', my_table.c.data, mysql_prefix='FULLTEXT') 指定索引前缀
        # Index('my_index', my_table.c.data, mysql_using='hash') 指定索引类型
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    password = Column(String(100))

    def __repr__(self):
        return f"<User(id={self.id} name={self.name})>"


class SqlHelper(object):
    def __init__(self, conn_str, ):
        self.engine = create_engine(
            fr'sqlite:///{conn_str}',
            echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_all_table(self):
        Base.metadata.create_all(self.engine)

    def test_add(self):
        """ 增加记录。"""
        ed_user = User(name='ed', password='as')
        self.session.add(ed_user)  # 将该实例插入到users表
        self.session.add_all(
            [User(name='ed1', password=None),
             User(name='ed2', password='password2'),
             User(name='ed3', password='password3')]
        )
        self.session.commit()  # 当前更改只是在session中，需要使用commit确认更改才会写入数据库

    def test_delete(self):
        """ 删除记录。"""
        firm = self.session.query(User).first()
        self.session.delete(firm)
        self.session.commit()

    def test_update(self):
        """ 修改记录。 """
        import random
        user = self.session.query(User).first()
        old_name = user.name
        new_name = f"fakename{random.random()}"
        print(f'oldname: {old_name}  new_name: {new_name}')
        self.session.commit()
        self.t

    def test_query(self):
        """ 查询记录。"""
        firm = self.session.query(Firm).filter(Firm.content.isnot(None)).first()
        print(f'first item: {firm}')
        school = self.session.query(Firm).filter(Firm.content.like(f"%{to_unicode_ascii('中学')}%")).count()
        print(f'school item count: {school}')

    def execute(self, sql):
        """
        执行原生SQL。
        :param sql:
        :return:
        """
        conn = self.engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()  # 需要手动关闭？？
        conn.close()  # 需要手动关闭？？
        return result


def test_helper():
    """

    :return:
    """
    helper = SqlHelper(conn_str=r'F:\workspace\gitee	echnology\python\examples\pyqt-exampleibiSpideribi.db')
    helper.create_all_table()
    data = helper.execute("select * from main.sqlite_master;")
    print(data)
    helper.test_add()


if __name__ == '__main__':
    test_helper()

