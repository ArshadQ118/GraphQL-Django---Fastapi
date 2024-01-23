from django.contrib.auth.hashers import make_password
from .models import User
import graphene


class UserType(graphene.ObjectType):
    class Meta:
        model = User
        fields = '__all__'


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, name, email, password):
        if name == "" or email == "" or password == "":
            raise Exception("Fields name and email are required")

        hashed_password = make_password(password)
        user = User(
            name=name,
            email=email,
            password=hashed_password,
        )
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, id, name, email):
        if id is None or id == "":
            raise Exception("Id is required")

        if name == "" or email == "":
            raise Exception("Fields name and email are required")

        userExist = User.objects.filter(id=id).exists()
        if not userExist:
            raise Exception("user does not exist")
        user = User.objects.get(pk=id)
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        user.save()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, id):
        if id is None or id == "":
            raise Exception("id is required")
        userExist = User.objects.filter(pk=id).exists()
        if not userExist:
            raise Exception("User does not exist")

        user_exist = User.objects.filter(pk=id).exists()
        if not user_exist:
            raise Exception("User does not exist")

        user = User.objects.get(pk=id)
        user.delete()
        return {}


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
