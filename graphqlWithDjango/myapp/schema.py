from .mutation import Mutation
from graphene import Schema
from .Query import Query

schema = Schema(query=Query, mutation=Mutation)
