from .builder import builder
from graphene import ObjectType

query_class = builder.build_schema_query()


class Query(query_class, ObjectType):
    pass
