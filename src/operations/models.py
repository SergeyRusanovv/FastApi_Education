from sqlalchemy import Column, Integer, String, TIMESTAMP, MetaData
from sqlalchemy.ext.declarative import declarative_base


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Operation(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=False)
    date = Column(TIMESTAMP)
    type = Column(String)
