from flask import Flask
from flask_graphql import GraphQLView
from flask_app.api import schema, session
from sqlalchemy.orm import scoped_session

# this is the flask application that is used to load the graphql api
# the api is imported from the flask_app.api
# the first thing that is imported is schema which is the graphql schema for the queries
# the session is the SQLAlchemy session that is used to connect to the database
app = Flask(__name__)

db_session = scoped_session(
    session
)

app.add_url_rule('/graphiql',  # the endpoint

                 # setting the view function
                 view_func=GraphQLView.as_view(
                     'graphql',

                     # we set the schema that we generate
                     schema=schema,

                     # We say that we *do* want a graphiql interface
                     graphiql=True
                 )
                 )


@app.teardown_appcontext
def remove_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
