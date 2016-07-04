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
	add_owner = Column(String(250),nullable=False)
	
	@property
	def serialize(self):
	#Return object data in easily serializeable format
		return{
			'id' : self.id,
			'name' : self.name,
			'add_owner' : self.add_owner
		}

class FootballClub(Base):
	__tablename__ = 'footballclubs'
	id = Column(Integer,primary_key=True)
	name = Column(String(250),nullable=False)
	country_id = Column(Integer,ForeignKey('countries.id'))
	add_owner = Column(String(250),nullable = False)
	country = relationship(Country)

	@property
	def serialize(self):
		return {
	        'id' : self.id,
	        'name' : self.name,
	        'country_id' : self.country_id,
	        'add_owner' : self.add_owner	
		}
	
engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)