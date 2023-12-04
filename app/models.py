from .database import Base
from sqlalchemy import Column, Integer, String,Float,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


# SQLAlchemy models
#Responsible for defining the columns of our "Locationsdata" table in postgres
# it is used to query,create,delete,update entries withing database

# Post will be longitude,latitude,name,description,created_by;

class Location(Base):
    __tablename__ = "locationsdata"

    locationid = Column(Integer, primary_key=True, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    name = Column(String, nullable=False) 
    description = Column(String, nullable=False)
    created_by = Column(String, nullable=False)  
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), 
                      nullable=False)
    
    
    owner = relationship("User")





class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

  