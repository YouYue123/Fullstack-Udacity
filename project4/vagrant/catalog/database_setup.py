import sys

from sqlalchemy import Column,ForeignKey,Integer,String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
	__tablename__ = 'users'
	id = Column(Integer,primary_key = True)
	name = Column(String(250),nullable = False)
	email = Column(String(250))
	password = Column(String(250),nullable=False)


class Catalog(Base):
	__tablename__ = 'catalogs'
	id = Column(Integer,primary_key= True)
	name = Column(String(250),nullable=False)


class Item(Base):
	__tablename__ = 'items'
	id = Column(Integer,primary_key=True)
	name = Column(String(250),nullable=False)
	content = Column(String(250),nullable=False)
	catalog = relationship(Catalog)
	owner = relationship(User)

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)