from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

from .models import CustomUser, CodeConfirmation
from rest_framework import permissions, status
from .serializers import UserSerializer

from helpers import send_sms, random_password
from helpers.random_password import generate_code_token


class RegisterApiView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        full_name = request.data.get('full_name')
        username = request.data.get('username')
        age = request.data.get('age')
        gender = request.data.get('gender')
        password = request.data.get('password')

        if CustomUser.objects.filter(email=email):
            return Response({'message': 'Bu email orqali oldin ro`yxatdan o`tilgan!'})

        user = CustomUser.objects.create(
            email=email,
            full_name=full_name,
            username=username,
            age=age,
            gender=gender,
            password=make_password(password)
        )
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class LoginStartView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            code = random_password.random_password(6)
            code_token = generate_code_token(32)
            CodeConfirmation.objects.create(
                user=user,
                code=code,
                code_token=code_token
            )
            send_sms.send_email(send_email=email,
                                message=f'Bizning tizimga kirish uchun kod {code}. Bu kodni hechkimga bermang!')
            return Response({
                'code_token': code_token
            })
        else:
            return Response({
                'Email or password incorrect!'
            })


class LoginEndView(APIView):
    def post(self, request):
        code = request.data.get('code')
        code_token = request.data.get('code_token')
        code_conf = CodeConfirmation.objects.filter(code_token=str(code_token)).first()

        if code_conf.code == code and code_conf.code_token == code_token:
            user = code_conf.user
            refresh = RefreshToken.for_user(user)
            code_conf.delete()

            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        else:
            return Response({'error':'code or code_token is wrong!'})
