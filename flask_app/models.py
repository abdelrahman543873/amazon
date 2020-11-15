from scrapy.utils.project import get_project_settings
from sqlalchemy import (
    Integer, Text)
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def db_connect():
    """
    this function returns the configuration of the database using the CONNECTION_STRING
    the CONNECTION_STRING is defined in the settings.py file
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


"""
    this is the table that is created in the database
"""


class Scraped(Base):
    __tablename__ = 'scraped'

    id = Column(Integer, primary_key=True)
    image_urls = Column('image_urls', Text())
    link = Column('link', Text())
    title = Column('title', Text())
    rating = Column('rating', Text())
    no_of_reviews = Column('no_of_reviews', Text())
    description = Column('description', Text())
    comments = Column('comments', Text())
    rating_distribution = Column('rating_distribution', Text())
    features = Column('features', Text())
