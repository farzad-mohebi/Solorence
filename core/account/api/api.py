import os
import datetime
import random
import string
import re

from django.contrib.auth.models import update_last_login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from google.auth.exceptions import GoogleAuthError
from google.oauth2.id_token import verify_token
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer

from account.api.serializers import UserSerializer, UserSignUpSerializer
from account.models import User
from core import settings
from utils.mail import MailService
from utils.response import ResponseNotOk, ResponseOk, BadRequest
from utils.viewset import CustomModelViewSet
from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, Http404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from google.auth.transport import requests
from django.core.cache import cache


class UserViewSet(CustomModelViewSet):
    model = User
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    def get_object(self):
        if self.action == 'self':
            return self.request.user
        return super().get_object()

    @action(methods=['get'], detail=False, serializer_class=UserSerializer,
            permission_classes=[permissions.IsAuthenticated])
    def self(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['put'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        user = self.request.user
        old_password = self.request.data.get('old_password')
        new_password = self.request.data.get('new_password')
        if not user.is_authenticated or not check_password(old_password, user.password):
            return ResponseNotOk(reason="invalid current password")
        user.password = make_password(new_password)
        user.save()
        login(request, user)
        return ResponseOk(detail="password changed")

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny])
    def send_forgot_password(self, req, *args, **kwargs):
        email = self.request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise BadRequest(detail='There is no user with this specifications!')
        front_url = os.getenv('FRONT_URL') or req.META.get('HTTP_ORIGIN')
        if cache.get('FORGOT_PASSWORD_' + str(user.id)):
            raise BadRequest(detail="You requested a password recently!")
        hash_code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        cache.set('FORGOT_PASSWORD_' + str(user.id), hash_code, 600)
        link = f'{front_url}/fp/{str(user.id)}/{hash_code}'
        print(f'Change Password Link: {link}')
        # config.get('class')(attr).send_forgot_link(token_id_hash, hash_code)
        return ResponseOk({})

    @action(methods=['put'], detail=False, permission_classes=[permissions.AllowAny])
    def change_forgot_password(self, request, *args, **kwargs):
        new_password = request.data.get('new_password')
        hash_code = request.data.get('hash_code')
        hash_id = request.data.get('hash_id')  # user id
        if not new_password or len(new_password) <= 5:
            raise BadRequest(detail="weak password")
        if not hash_code or not hash_id:
            raise BadRequest(detail="invalid hash_code and hash_id")
        if cache.get('FORGOT_PASSWORD_' + str(hash_id)) != hash_code:
            raise BadRequest(detail="expired, try again")
        user = User.objects.filter(id=hash_id).first()
        if not user:
            raise BadRequest(detail="expired, try again")
        user.password = make_password(new_password)
        user.save()
        cache.delete('FORGOT_PASSWORD_' + str(hash_id))
        return ResponseOk()

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny])
    def send_signup(self, req, *args, **kwargs):
        email = self.request.data.get('email')
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise BadRequest(detail='invalid email!')
        user = User.objects.filter(email=email.lower()).first()
        if user:
            raise BadRequest(detail='this account already exists!')
        front_url = os.getenv('FRONT_URL') or req.META.get('HTTP_ORIGIN')
        if cache.get('SIGN_UP_' + str(user)):
            raise BadRequest(detail="You requested a password recently!")
        hash_code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        cache.set('SIGN_UP_' + email, hash_code, 600)
        link = f'{front_url}verify/{str(email)}/{hash_code}'
        print(f'Verify Account: {link}')
        sent_status = MailService().send_signup_link(email, link)
        if not sent_status:
            cache.delete('SIGN_UP_' + str(user))
            raise BadRequest(detail='send email failed! please try again')
        # config.get('class')(attr).send_forgot_link(token_id_hash, hash_code)
        return ResponseOk({})

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny])
    def signup(self, req, *args, **kwargs):
        hash_code = self.request.data.get('hash_code')
        email = self.request.data.get('email')
        state = self.request.data.get('state')
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise BadRequest(detail='invalid email!')
        if not hash_code:
            raise BadRequest(detail='invalid hash code!')
        if not cache.get('SIGN_UP_' + email):
            raise BadRequest(detail='your signup has been expired!')
        if cache.get('SIGN_UP_' + email) != hash_code:
            raise BadRequest(detail='invalid link!')
        if state == 'check':
            return ResponseOk()
        serializer = UserSignUpSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token_for_user = RefreshToken.for_user(serializer.instance)
        return Response({
            'refresh': str(token_for_user),
            'access': str(token_for_user.access_token),
        }, status=status.HTTP_200_OK)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = []

    @swagger_auto_schema(
        method='post',
        request_body=TokenObtainPairSerializer,
    )
    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=self.request.data)
        serializer.password = make_password(self.request.data['password'])
        if config.get('picture'):
            self.request._files.get(config.get('picture'))
        username = self.request.data.get(config.get('user_key'))
        mobile_number = self.request.data.get('mobile_number')
        email = self.request.data.get('email')
        password = self.request.data.get('password')

        # Email
        if User.objects.filter(email=email).first():
            return Response({'email': [_('This mobile number already registered'), ]},
                            status=status.HTTP_400_BAD_REQUEST)
        if not config['email_validator'](email):
            return Response({'email': ['Invalid mobile number']},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        user = serializer.instance
        user.password = make_password(password)
        user.username = username
        token = Token()
        user.email = email
        token.email = email
        user.save()
        token.token = random_with_N_digits(5)
        token.last_send = timezone.now()
        if config.get('sms_panel'):
            config['sms_panel'](mobile_number).send_verify_code(token.token)
        if config.get('email_panel'):
            config['email_panel'](email).send_verify_code(token.email)
        token.save()
        user.token = token
        user.save()
        refresh = RefreshToken.for_user(user)
        return ResponseOk(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    @action(methods=['post'], detail=False)
    def resend(self, request, *args, **kwargs):
        config = BADI_AUTH_CONFIG['resend']
        if not config['is_active']:
            return Http404()
        data = request.data.get(config['user_find_key'])
        user = User.objects.filter(**{config['user_find_key']: data}).first()
        if not user:
            return ResponseNotOk(reason=config['errors']['404'])
        user_attr = getattr(user, config['user_find_key'])
        token = Token.objects.filter(**{config['token_key']: user_attr}).last()
        if token and token.is_active():
            if token.is_possible_resend():
                config['class'](user_attr).send_verify_code(token.token)
                token.last_send = datetime.datetime.now()
                token.save()
            else:
                return ResponseNotOk(reason=_(BadiErrorCodes.sms_send_recently))
        else:
            token = Token()
            token.token = random_with_N_digits(5)
            setattr(token, config['token_key'], user_attr)
            token.last_send = datetime.datetime.now()
            config['class'](user.mobile_number).send_verify_code(token.token)
            token.save()

        return ResponseOk()

    @action(methods=['post'], detail=False)
    def verify(self, request, *args, **kwargs):
        config = BADI_AUTH_CONFIG['verify']
        if not config['is_active']:
            return Http404()
        data = request.data.get(config['user_find_key'])
        code = request.data.get('code')
        token = Token.objects.filter(**{config['user_find_key']: data}, is_accepted=False).last()
        if not token:
            return ResponseNotOk(reason=_(BadiErrorCodes.not_found))
        if not token.is_active():
            return ResponseNotOk(reason=_(BadiErrorCodes.expired))
        if token.token != code:
            return ResponseNotOk(reason=_(BadiErrorCodes.wrong_code))
        user = User.objects.filter(**{config['user_key']: data}).first()
        refresh = RefreshToken.for_user(user)
        token.is_accepted = True
        token.save()
        Token.objects.filter(created_at__lt=datetime.datetime.now() - timedelta(hours=24)).delete()
        login(self.request, user)
        return ResponseOk(detail={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    @action(methods=['post'], detail=False)
    def refresh(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GoogleAuthReceiver(APIView):
    permission_classes = [permissions.AllowAny]
    """
    Google calls this URL after the user has signed in with their Google account.
    """

    def post(self, request, *args, **kwargs):
        token = request.data['credential']
        try:
            idinfo = verify_token(
                token,
                requests.Request(),
                audience=settings.GOOGLE_OAUTH_CLIENT_ID,
                certs_url='https://www.googleapis.com/oauth2/v1/certs',
                clock_skew_in_seconds=0,
            )

            if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
                raise GoogleAuthError(
                    "Wrong issuer. 'iss' should be one of the following: {}".format(
                        ["accounts.google.com", "https://accounts.google.com"]
                    )
                )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            if idinfo.get('email') and idinfo.get('email_verified'):
                response = {}
                user, is_created = User.objects.get_or_create(email=idinfo.get('email'), defaults={
                    'first_name': idinfo.get('given_name'),
                    'last_name': idinfo.get('family_name'),
                    'username': idinfo.get('email').split('@')[0],
                })
                refresh = TokenObtainPairSerializer.get_token(user)
                response['refresh'] = str(refresh)
                response['access'] = str(refresh.access_token)

                update_last_login(None, user)

                return Response(response)

            return ResponseNotOk(reason="unverified email!")
        except ValueError as err:
            # Invalid token
            print(err)
            content = {'message': 'Invalid token'}
            return ResponseNotOk(content)
