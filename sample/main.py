# from graphene import ObjectType, String, Schema, Int
# from starlette_graphene3 import GraphQLApp, make_graphiql_handler
# from typing import Union
# from fastapi import FastAPI
#
#
# class Calculator(ObjectType):
#     concat = String(a=String(), b=String())
#     add = String(a=Int(), b=Int())
#
#     def resolve_concat(self, info, a, b):
#         return a + " " + b
#
#     def resolve_add(self, info, a, b):
#         return int(a + b)
#
#
# app = FastAPI()
#
# app.mount("/", GraphQLApp(schema=Schema(query=Calculator), on_get=make_graphiql_handler()))
#
#
# # app.add_route("/", GraphQLApp(schema=Schema(query=Calculator), on_get=make_graphiql_handler()))
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from graphene import ObjectType, String, Field, List, Schema
from mutation import CreateUser, UpdateUser, DeleteUser
from fastapi import FastAPI
from query import Query
from type import User

app = FastAPI()


class MyMutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


class MyQuery(Query):
    user = Field(User)
    get_user = Field(User, id=String())
    get_users = List(User)


schema = Schema(query=MyQuery, mutation=MyMutation)
# createUser_Obj = schema.execute(
#     '''
#     mutation {
#       createUser(id: "2", name: "John Doe", email: "user@example.com", password: "password") {
#         user {
#           id
#           name
#           email
#         }
#       }
#     }
#     '''
# )
#
# print("createUser_Obj", createUser_Obj.data)

# updateUser_obj = schema.execute(
#     '''
#     mutation {
#         updateUser(id: "1", name: "John Smith", password: "password", email: "meial@gmail.com") {
#             user {
#                 id
#                 name
#                 email
#                 password
#             }
#         }
#     }
#     '''
# )
# print("updateUser", updateUser_obj.data)

# deleteUser_obj = schema.execute(
#     '''
#     mutation {
#         deleteUser(id: "1") {
#             user {
#                 id
#                 name
#                 email
#                 password
#             }
#         }
#     }
#     '''
# )
#
# print(deleteUser_obj.data)

getUser_obj = schema.execute(
    '''
    query {
        getUser (id: "1") {
            id
            name
            email
            password
        }
    }
    '''
)
print("getUser_obj", getUser_obj.data)


getUsers_obj = schema.execute(
    '''
    query {
        getUsers {
            id
            name
            email
            password
        }
    }
    '''
)
print(getUsers_obj.data)

app.mount("/", GraphQLApp(schema=Schema(query=MyQuery, mutation=MyMutation), on_get=make_graphiql_handler()))
