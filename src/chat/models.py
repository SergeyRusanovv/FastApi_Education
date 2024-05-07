from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Messages(Base):
	__tablename__ = "messages"

	id = Column(Integer, primary_key=True)
	message = Column(String)
