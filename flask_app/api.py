from graphene import ObjectType, Field, ID, Schema, List,  String, Int
from graphene.types.mutation import Mutation
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
        return session.query(Scraped).get(args.get('id'))

    def resolve_allProducts(self, args, context, info):
        return session.query(Scraped).order_by(Scraped.id).all()


class CreateProduct(Mutation):

    class Input:
        image_urls = String(required=True)
        link = String(required=False)
        title = String(required=False)
        rating = String(required=False)
        no_of_reviews = String(required=False)
        description = String(required=False)
        comments = String(required=False)
        rating_distribution = String(required=False)
        features = String(required=False)

    product = Field(Product)

    @classmethod
    def mutate(cls, _, context, **args):
        scraped = Scraped()
        scraped.image_urls = args.get('image_urls')
        scraped.link = args.get('link')
        scraped.title = args.get('title')
        scraped.rating = args.get('rating')
        scraped.no_of_reviews = args.get('no_of_reviews')
        scraped.description = args.get('description')
        scraped.comments = args.get('comments')
        scraped.rating_distribution = args.get('rating_distribution')
        scraped.features = args.get('features')
        session.add(scraped)
        session.commit()
        return CreateProduct(product=scraped)


class DeleteProduct(Mutation):

    class Input:
        id = Int(required=True)

    product = Field(Product)

    @classmethod
    def mutate(cls, _, args, context, info):
        query = session.query(Scraped).get(args['id'])
        session.delete(query)
        session.commit()
        return DeleteProduct(product=query)


class Mutation(ObjectType):
    create_product = CreateProduct.Field()
    delete_product = DeleteProduct.Field()


schema = Schema(query=Query, mutation=Mutation)
