# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import TakeFirst, MapCompose


def remove_quotes(text):
    # strip the unicode quotes
    text = text.strip(u'\u201c'u'\u201d')
    return text


class AmazonItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = Field(input_processor=MapCompose(remove_quotes),
                       output_processor=TakeFirst())
    link = Field(input_processor=MapCompose(remove_quotes),
                 output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(remove_quotes),
                  output_processor=TakeFirst())
    rating = Field(input_processor=MapCompose(remove_quotes),
                   output_processor=TakeFirst())
    no_of_reviews = Field(input_processor=MapCompose(remove_quotes),
                          output_processor=TakeFirst())
    description = Field(input_processor=MapCompose(remove_quotes),
                        output_processor=TakeFirst())
    comments = Field(input_processor=MapCompose(remove_quotes),
                     output_processor=TakeFirst())
    rating_distribution = Field(input_processor=MapCompose(remove_quotes),
                                output_processor=TakeFirst())
    features = Field(input_processor=MapCompose(remove_quotes),
                     output_processor=TakeFirst())
