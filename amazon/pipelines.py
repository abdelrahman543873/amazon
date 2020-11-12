# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from flask_app.models import Scraped, db_connect, create_table


class AmazonPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        scraped = Scraped()
        scraped.image_urls = item['image_urls']
        scraped.link = item['link']
        scraped.title = item['title']
        scraped.rating = item['rating']
        scraped.no_of_reviews = item['no_of_reviews']
        scraped.description = item['description']
        scraped.comments = item['comments']
        scraped.rating_distribution = item['rating_distribution']
        scraped.features = item['features']
        try:
            session.add(scraped)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
