from graphene import ObjectType, String, ID, Int, Float, Boolean


class User(ObjectType):
    id = String()
    name = String()
    email = String()
    password = String()
