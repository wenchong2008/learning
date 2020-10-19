# /user/bin/env python
__author__ = 'wenchong'


from config import setting
import datetime

from sqlalchemy import create_engine, Column, Integer, \
    String, ForeignKey, ForeignKeyConstraint, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class UserToGroup(Base):
    __tablename__ = 'user_group'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    group_id = Column(Integer, ForeignKey('group.id'))


class HostUserToGroup(Base):
    __tablename__ = 'host_user_group'
    id = Column(Integer, autoincrement=True, primary_key=True)
    hostuser_id = Column(Integer,ForeignKey('host_user.id'))
    group_id = Column(Integer, ForeignKey('group.id'))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    password = Column(String(32), nullable=False)
    groups = relationship('Group', secondary=UserToGroup.__table__)

    def __repr__(self):
        return "<User:id=%s,name=%s>" % (self.id, self.name)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    users = relationship('User', secondary=UserToGroup.__table__)
    hostusers = relationship('HostUser', secondary=HostUserToGroup.__table__)

    def __repr__(self):
        return "<Group:id=%s,name=%s>" % (self.id, self.name)


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, autoincrement=True, primary_key=True)
    hostname = Column(String(64), unique=True, nullable=False)
    ip_address = Column(String(16), unique=True, nullable=False)

    host_users = relationship('HostUser', backref='host')

    def __repr__(self):
        return "<Host:id=%s,hostname=%s,ip:%s>" % (self.id, self.hostname, self.ip_address)


class HostUser(Base):
    __tablename__ = 'host_user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(32), nullable=False)
    password = Column(String(64), nullable=False)

    host_id = Column(Integer, ForeignKey('host.id'))

    groups = relationship('Group', secondary=HostUserToGroup.__table__)

    __table_args = (
        UniqueConstraint('username', 'host_id'),
    )

    def __repr__(self):
        return "<HostUser:id=%s,username=%s>" % (self.id, self.username)

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, autoincrement=True, primary_key=True)
    add_time = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('user.id'))
    hostuser_id = Column(Integer, ForeignKey('host_user.id'))
    command = Column(String(255), nullable=False)


class ModelAdmin(object):
    """Model Admin For Add Host, HostUser, User, Group ..."""
    def __init__(self):
        self.db_user = setting.DB_USER
        self.db_pass = setting.DB_PASS
        self.db_host = setting.DB_HOST
        self.db_name = setting.DB_NAME

        self.engine = create_engine(
            "mysql+pymysql://{user}:{password}@{host}:3306/{db_name}".format(
                user=setting.DB_USER,
                password=setting.DB_PASS,
                host=setting.DB_HOST,
                db_name=setting.DB_NAME
            ),
            max_overflow=5  # connection pool
        )

        self.init_db()

    def init_db(self):
        self.create_table()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_table(self):
        """创建所有的表"""
        Base.metadata.create_all(self.engine)

    def drop_table(self):
        """删除所有的表"""
        Base.metadata.drop_all(self.engine)

    def get_host_for_ip(self, ip_address):
        return self.session.query(Host).filter(Host.ip_address == ip_address).first()

    def get_host_for_hostname(self, hostname):
        return self.session.query(Host).filter(Host.hostname == hostname).first()

    def get_group(self, name=None):
        if name:
            return self.session.query(Group).filter(Group.name == name).first()
        else:
            return self.session.query(Group).all()

    def get_host_user(self):
        return self.session.query(HostUser).all()

    def get_user(self, name):
        return self.session.query(User).filter(User.name == name).first()

    def add_host(self, hostname, ip_address, username, password):
        """add host for hostname ,ip address, username, password"""
        host_obj = self.get_host_for_ip(ip_address)
        if host_obj:
            # change hostname
            if host_obj.hostname != hostname:
                host_obj.hostname = hostname

            host_user_obj = self.session.query(HostUser).filter(
                HostUser.host_id == host_obj.id, HostUser.username == username).first()

            if host_user_obj:
                # change password for username
                if host_user_obj.password != password:
                    host_user_obj.password = password

            else:
                host_obj.host_users.append(
                    HostUser(username=username, password=password)
                )

        else:
            host_obj = Host(hostname=hostname, ip_address=ip_address)
            host_obj.host_users.append(
                HostUser(username=username, password=password)
            )
            self.session.add(host_obj)

        self.commit()

    def add_user(self, name, password):
        """add system user"""
        user_obj = self.get_user(name)
        if not user_obj:
            user_obj = User(name=name, password=password)
            self.session.add(user_obj)

        else:
            if user_obj.password != password:
                user_obj.password = password

        return user_obj

    def add_group(self, name):
        """add group"""
        group_obj = self.get_group(name)
        if not group_obj:
            group_obj = Group(name=name)
            self.session.add(group_obj)
            # self.commit()
        return group_obj

    def add_log(self, user, host_user, command):

        log_obj  = Log(user_id=user, hostuser_id=host_user, command=command)
        self.session.add(log_obj)
        self.session.commit()

    def commit(self):
        self.session.commit()
