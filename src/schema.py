import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User, Session


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    user = graphene.Field(UserType, id=graphene.String())
    users = graphene.List(UserType)

    def resolve_user(self, info, id):
        session = Session()
        user = session.query(User).get(id)
        session.close()
        return user

    def resolve_users(self, info):
        session = Session()
        users = session.query(User).all()
        session.close()
        return users


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: UserType)

    def mutate(self, info, name, email, password):
        session = Session()
        user = User(name=name, email=email, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(lambda: UserType)

    def mutate(self, info, id, **kwargs):
        session = Session()
        user = session.query(User).get(id)
        if user is None:
            session.close()
            raise Exception(f"User with id {id} not found")

        for key, value in kwargs.items():
            setattr(user, key, value)

        session.commit()
        session.refresh(user)
        session.close()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    user = graphene.Field(lambda: UserType)

    def mutate(self, info, id):
        session = Session()
        user = session.query(User).get(id)
        if user is None:
            session.close()
            raise Exception(f"User with id {id} not found")

        session.delete(user)
        session.commit()
        session.close()
        return DeleteUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
