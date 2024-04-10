from django.contrib.auth import authenticate, login, logout
import requests
from config import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework import exceptions
import jwt
from . import serializers
from .models import User as USER

class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):

    def post(self, request):
        password = request.data.get['password']
        if not password:
            raise exceptions.ParseError

        user = request.data
        serializer = serializers.PrivateUserSerializer(data=user)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):

    def get_user(self, username):
        try:
            user = USER.objects.get(username=username)
            return user
        except USER.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, username):
        user = self.get_user(username)
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)



class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not (old_password or new_password):
            raise exceptions.ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not (username or password):
            raise exceptions.ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "welcome"})
        else:
            return Response({"error": "wrong password"})

class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok" : "bye!"})


class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not (username or password):
            raise exceptions.ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm=["HS256"],
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})

class GithubLogIn(APIView):

    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(f"https://github.com/login/oauth/access_token?code={code}&client_id=7a2d6e687ddb017273ff&client_secret={settings.GH_SECRET}",
                                         headers={"Accept" : "application/json"})
            access_token = access_token.json().get("access_token")
            user_data = requests.get("https://api.github.com/user",
                                     headers={"Authorization" : f"Bearer {access_token}", "Accept" : "application/json"})
            user_email = requests.get("https://api.github.com/user/emails",
                                      headers={"Authorization" : f"Bearer {access_token}", "Accept" : "application/json"})
            user_data = user_data.json()
            user_email = user_email.json()

            try:
                user = USER.objects.get(email=user_email[0]['email'])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except USER.DoesNotExist:
                user = USER.objects.create(
                    username=user_data.get('login'),
                    email=user_email[0]['email'],
                    name=user_data.get('name'),
                    profile_photo=user_data.get('avatar_url'),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class KakaoLogIn(APIView):

    def post(self, request):

        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "fcc696f712982887c4bfd776d82dbb0c",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                    "client_secret": "ZXmDBuoHv5X2umwoletvKeYyC1XFy00H"
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get("https://kapi.kakao.com/v2/user/me",
                                     headers={"Authorization": f"Bearer {access_token}",
                                              "Content-type": "application/x-www-form-urlencoded;charset=utf-8"})
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = USER.objects.get(username=profile.get('nickname'))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except USER.DoesNotExist:
                user = USER.objects.create(
                    username=profile.get("nickname"),
                    profile_photo=profile.get("profile_image_url")
                )
                user.set_unusable_password()
                user.save()
                login(user, request)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
