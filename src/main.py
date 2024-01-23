# main.py
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from fastapi import FastAPI
from schema import schema

app = FastAPI()

# Mount the GraphQL app at the endpoint '/graphql'
app.mount("/", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
