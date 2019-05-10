from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import Date, Boolean

engine = create_engine('mysql://root@localhost:3306/shiyanlou?charset=utf8')

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    # 默认False即普通用户，True则表示会员用户
    is_vip = Column(Boolean, default=False)
    status = Column(String(64), index=True)
    school_job = Column(String(64))
    level = Column(Integer, index=True)
    join_date = Column(Date)
    learn_courses_num = Column(Integer)
    

class Course(Base):
    
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    description = Column(String(1024))
    type = Column(String(64), index=True)
    students = Column(Integer)
    
if __name__ == '__main__':
    Base.metadata.create_all(engine)