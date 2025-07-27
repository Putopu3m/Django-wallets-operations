from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import UserSerializer

User = get_user_model()

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer