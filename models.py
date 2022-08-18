#imports
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#build engines and other important things
engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Create Databases

class Brand(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column("Brand Name", String)

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column("Product Name", String)
    product_quantity = Column("Product Quantity", Integer)
    product_price = Column("Product Price", Integer)
    date_updated = Column("Date Updated", DateTime)
    brand_name = Column("Brand Name", String)
    brand_id = Column(Integer, ForeignKey(Brand.brand_id))
