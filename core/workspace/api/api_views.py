import datetime

from django.shortcuts import redirect
from django.http import JsonResponse
import requests
import json
from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.apps import meet_v2
from django.conf import settings
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.viewset import CustomModelViewSet
from workspace.api.serializers import *
from workspace.filter import *
from workspace.models import *
from google.oauth2.service_account import Credentials as ServiceCredentials

# Define the scopes for Google Meet API
SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']
SERVICE_ACCOUNT_FILE = settings.GOOGLE_AUTH_FILES_DIR  # مسیر فایل سرویس اکانت

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_API_URL = "https://www.googleapis.com/calendar/v3"


class GoogleMeetCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:

            # Load service account credentials
            creds = ServiceCredentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

            # Create a Google Meet space
            client = meet_v2.SpacesServiceClient(credentials=creds)
            create_request = meet_v2.CreateSpaceRequest()
            response = client.create_space(request=create_request)

            # Return the meeting link as JSON response
            return JsonResponse({'meeting_link': response.meeting_uri})

        except Exception as e:
            print("=========== Exception", e)
            return JsonResponse({'error': str(e)}, status=500)


# 1. دریافت authorization code و تبادل آن با access token
class ExchangeGoogleTokenApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')

        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }

        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        token_data = response.json()

        if 'access_token' in token_data:
            # ذخیره کردن access token در سرور برای استفاده در درخواست‌های بعدی
            request.session['google_access_token'] = token_data['access_token']
            return JsonResponse({'access_token': token_data['access_token']})
        else:
            return JsonResponse({'error': 'Failed to exchange code for token'}, status=400)


# 2. ایجاد رویداد Google Calendar
class CreateMeetEventApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        access_token = request.data.get('google_access_token')
        if not access_token:
            return JsonResponse({'error': 'Unauthorized Google Token!'}, status=401)
        at = datetime.datetime.strptime(f"{request.data['date']} {request.data['time']}", '%Y-%m-%d %H:%M')
        done = at + datetime.timedelta(minutes=int(request.data['duration']))

        tz = datetime.timezone(datetime.timedelta(hours=-7))
        at = at.replace(tzinfo=tz)

        tz = datetime.timezone(datetime.timedelta(hours=-7))
        done = done.replace(tzinfo=tz)

        event = {
            'summary': request.data.get('title'),
            'start': {
                'dateTime': at.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': done.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': 'sample123',
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                }
            },
        }
        print(event)
        # return Response()
        credentials = Credentials(token=access_token)
        try:
            service = build('calendar', 'v3', credentials=credentials)
            result = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
            print("result EVENT DATA: ", result)
            return JsonResponse(result)
        except HttpError as error:
            return JsonResponse({'error': str(error)}, status=400)
