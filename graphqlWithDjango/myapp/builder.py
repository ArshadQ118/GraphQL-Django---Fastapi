from django_graphbox.builder import SchemaBuilder
from .models import User

builder = SchemaBuilder()
builder.add_model(User)
