import graphene
from type import User
from data import users


class CreateUser(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(root, info, id, name, email, password):
        user = User(id=id, name=name, email=email, password=password)
        users.append({
            "id": id,
            "name": name,
            "email": email,
            "password": password
        })
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(self, info, id, name, password, email):
        user = User(id=id, name=name, email=email, password=password)
        old_user = list(filter(lambda user: user["id"] == id, users))[0]
        users.remove(old_user)
        users.append({
            "id": id, "name": name, "email": email, "password": password
        })
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(self, info, id):
        old_user = list(filter(lambda user: user["id"] == id, users))[0]
        user = User(id=old_user["id"], name=old_user["name"], email=old_user["email"], password=old_user["password"])
        users.remove(old_user)
        return DeleteUser(user=user)
