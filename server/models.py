from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

Base = declarative_base()

class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    account = Column(String(250))
    password = Column(String(250))
    Sclass = Column(String(250))
    result = Column(String(250))

class Clubs(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    max = Column(String(250))
    reject = Column(String(250))
    teacher = Column(String(250))
    location = Column(String(250))
    comment = Column(String(250))

class Chooses(Base):
    __tablename__ = 'chooses'
    id = Column(Integer, primary_key=True)
    stu_id = Column(String(250))
    step = Column(String(250))
    club_id = Column(String(250))

class Manage(Base):
    __tablename__ = 'manage'
    id = Column(Integer, primary_key=True)
    account = Column(String(250))
    password = Column(String(250))
    name = Column(String(250))
    status = Column(String(250))
    permission = Column(String(250))

engine = create_engine('mysql://{}:{}@{}:{}/{}?charset=utf8'.format(config.getConf('dbaccount'), config.getConf('dbpassword'), config.getConf('dbhost'), config.getConf('dbport'), config.getConf('database')), echo=True, encoding='utf-8', convert_unicode=True)
Base.metadata.create_all(engine)

def DB_session():
    return sessionmaker(engine)
