from graphene import ObjectType, Field, ID, Schema, String, List, Int
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from flask_app.models import Scraped, db_connect
from graphene_sqlalchemy import SQLAlchemyObjectType


engine = db_connect()
Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine)
session = Session()


"""
this is a graphene_sqlalchemy class called SQLAlchemyObjectType 
this allows you to have the graphql object of your model without having to 
define it if you want to know more about graphene_sqlalchemy read here
https://github.com/graphql-python/graphene-sqlalchemy
"""


class Product(SQLAlchemyObjectType):
    class Meta:
        model = Scraped


"""
this is the object type that is used for defining the query for graphql , here allProducts property is resolved using the 
resolve_allProducts and the same for the product property 
"""


class Query(ObjectType):
    allProducts = List(Product)
    product = Field(Product, id=ID())

    def resolve_product(self, args, context, info):
        return session.query(Scraped).filter(Scraped.id == args['id']).first()

    def resolve_allProducts(self, args, context, info):
        return session.query(Scraped).order_by(Scraped.id).all()


schema = Schema(query=Query)
