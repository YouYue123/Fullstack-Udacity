import sys

from sqlalchemy import Column,ForeignKey,Integer,String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Country(Base):
	__tablename__ = 'countries'
	id = Column(Integer,primary_key= True)
	name = Column(String(250),nullable=False)


class FootballClub(Base):
	__tablename__ = 'footballclubs'
	id = Column(Integer,primary_key=True)
	name = Column(String(250),nullable=False)
	country = relationship(Country)
	add_owner = Column(String(250),nullable = False)

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)