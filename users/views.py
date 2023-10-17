from rest_framework.views import APIView, Response, status, Request
from users.serializers import UserSerializer, LoginSerializer
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.authentication import TokenAuthentication
from users.permissions import IsAdmin


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except IntegrityError as e:
            if "UNIQUE" in str(e):
                return Response({"email": "aqui"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request):
        user = CustomUser.objects.all()

        serializer = UserSerializer(user, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class UserByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request: Request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)

            serializer = UserSerializer(user)

            return Response(serializer.data, status.HTTP_200_OK)

        except ObjectDoesNotExist as _:
            return Response({"message": "User not found."}, status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key})
        else:
            return Response(
                {"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED
            )
