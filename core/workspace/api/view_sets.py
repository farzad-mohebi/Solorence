import datetime

from google.oauth2.service_account import Credentials
from google.apps import meet_v2
from django.conf import settings
from django.http import JsonResponse, Http404
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.serializers import UserProfileSerializer
from utils.response import ResponseOk, BadRequest
from utils.viewset import CustomModelViewSet
from workspace.api.serializers import *
from workspace.api.serializers import NoteSecurityConfigSerializer
from workspace.filter import *
from workspace.history_structure import History
from workspace.models import *


class CustomPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = 'limit'
    max_page_size = 24


class NoteViewSet(CustomModelViewSet):
    model = Note
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_object(self):
        if self.action == 'update_other_note':
            note = Note.objects.prefetch_related('access', 'settings').filter(id=self.kwargs['pk']).first()
            note_access = note.access.filter(user_id=self.request.user.id).first()
            if note_access and note_access.access == AccessTypes.editor:
                return note
            setting: NoteSecurityConfig = note.get_settings()
            if setting.is_public and setting.public_joiners_access == AccessTypes.editor:
                return note
            raise PermissionDenied
        return super().get_object()

    def filter_queryset(self, qs):
        if self.action == 'update_other_note':
            pass
        elif self.action == 'accessible_notes':
            note_ids = [acc.note_id for acc in self.request.user.access.all()]
            return NoteFilter(self.request.query_params).qs.prefetch_related('settings').filter(id__in=note_ids)
        elif self.action in ['update', 'destroy', 'delete', 'retrieve']:
            return qs.filter(user=self.request.user)
        elif self.action == 'trash':
            return qs.filter(user=self.request.user, deleted_at__isnull=False)
        elif not self.request.user.is_superuser:
            return NoteFilter(self.request.query_params).qs.filter(user=self.request.user, deleted_at__isnull=True)
        return super().filter_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.deleted_at:
            instance.delete()
        else:
            instance.deleted_at = datetime.datetime.now()
            instance.save()

    @action(methods=['get'], detail=False, url_path='config/(?P<note_id>[^/.]+)')
    def config(self, request, note_id, *args, **kwargs):
        config = get_object_or_404(NoteSecurityConfig, note_id=note_id, note__user=self.request.user)
        return Response(NoteSecurityConfigSerializer(config).data)

    @action(methods=['get'], detail=False, url_path='history/(?P<note_id>[^/.]+)')
    def history(self, request, note_id, *args, **kwargs):
        note: Note = get_object_or_404(Note, pk=note_id, user=self.request.user)
        return Response(note.history)

    @action(methods=['post'], detail=False, url_path='set_history/(?P<note_id>[^/.]+)')
    def set_history(self, request, note_id, *args, **kwargs):
        note: Note = get_object_or_404(Note, pk=note_id, user=self.request.user)
        if note.history and type(note.history) == list:
            note.history.insert(0, History(
                title=note.title,
                blocks=note.editor_data,
                is_read_only=True
            ).get_dict())
            note.save()
        return ResponseOk()

    @action(methods=['get'], detail=False, url_path='get_data/(?P<link>[^/.]+)',
            permission_classes=[permissions.AllowAny])
    def get_data(self, request, link, *args, **kwargs):
        access = AccessTypes.viewer
        config: NoteSecurityConfig = NoteSecurityConfig.objects.prefetch_related('note').filter(link=link).first()
        data = NoteSerializer(config.note).data
        if not config:
            raise PermissionDenied(detail='You do not have permission to this note')
        user = self.request.user
        if not user.is_authenticated:  # Anonymous user ResponseOK() if note is public else Error
            if config.is_public:
                data['access'] = AccessTypes.viewer
                return Response(data)
            raise PermissionDenied(detail='You do not have permission to this note')

        if user.id == config.note.user_id:
            access = AccessTypes.editor
        elif note_access := NoteAccess.objects.filter(note=config.note, user=user).first():
            # if User has Access to this note
            if config.status == SecurityStatus.public and note_access.access <= config.status:
                # if User has Access was less than Note input users access
                note_access.access = config.status
                note_access.save()
            access = note_access.access
        elif user_invited := NoteRequestAccess.objects.filter(
                user=user, type=RequestType.invite, status=RequestAccessStatuses.pending).first():
            # User has been invited to this note
            note_access_invite, is_created = NoteAccess.objects.get_or_create(
                user=user,
                note=config.note,
                defaults={
                    "access": user_invited.access
                }
            )
            if not is_created and user_invited.access > note_access_invite.access:
                # if owner invited to higher permission then update access
                note_access_invite.access = user_invited.access
                note_access_invite.save()
            # Confirm user invite
            user_invited.status = RequestAccessStatuses.accepted
            user_invited.save()
            access = user_invited.access
        elif config.status == SecurityStatus.public:
            # Create access for user
            NoteAccess.objects.get_or_create(
                user=user,
                note=config.note,
                defaults={'access': config.public_joiners_access}
            )
            access = config.public_joiners_access
        else:
            return Response({
                'request_sent': NoteRequestAccess.objects.filter(
                    note_id=config.note_id, user=user, status=RequestAccessStatuses.pending).exists()
            })
        data['access'] = access
        return Response(data)

    @action(methods=['get'], detail=False, url_path='get_access_config/(?P<pk>[^/.]+)', )
    def get_access_config(self, request, pk, *args, **kwargs):
        user = self.request.user
        note = Note.objects.prefetch_related('settings', 'access', 'requests').filter(pk=pk, user=user).first()
        note_access_requests = note.requests.filter(type=RequestType.request, status=RequestAccessStatuses.pending)
        if not note:
            raise NotFound()
        note_config = note.get_settings()
        response = {
            'config': NoteSecurityConfigSerializer(note_config).data,
            'users': NoteAccessSerializer(note.access.all(), many=True).data,
            'requests': NoteRequestAccessSerializer(note_access_requests, many=True).data
        }
        response['users'].append({
            'user': UserProfileSerializer(user).data,
            'access': AccessTypes.editor,
        })
        return Response(response)

    @action(methods=['get'], detail=False, url_path='get_users/(?P<pk>[^/.]+)', )
    def get_users(self, request, pk, *args, **kwargs):
        user = self.request.user
        note_access_qs = NoteAccess.objects.prefetch_related('user').filter(
            note_id=pk,
            note__user=user
        )
        response = UserProfileSerializer([access.user for access in note_access_qs] + [user], many=True).data
        return Response(response)

    @action(methods=['post'], detail=False, url_path='(?P<note_id>[^/.]+)/grant_user', )
    def grant_user(self, request, note_id, *args, **kwargs):
        user = self.request.user
        owner_message = request.data.get('owner_message')
        is_notify = request.data.get('is_notify')
        email = request.data.get('email')
        if not email:
            raise BadRequest(detail='Invalid Email Address')

        access = request.data.get('access')
        if access not in [1, 2, 3]:
            raise BadRequest(detail='Invalid Access type')

        note = Note.objects.filter(pk=note_id, user=user).first()
        if not note:
            raise PermissionDenied(detail='You dont have permission to this note!')

        grant_user = User.objects.filter(email=email).first()
        if not grant_user:
            raise BadRequest(detail='User not found')

        grant, is_created = NoteAccess.objects.get_or_create(
            note=note,
            user=grant_user,
            defaults={'access': access}
        )
        if grant.access != access:
            grant.access = access
            grant.save()

        if is_notify:
            invite, is_created = NoteRequestAccess.objects.get_or_create(
                note=note,
                user=grant_user,
                owner_message=owner_message,
                type=RequestType.invite,
                defaults={'access': access}
            )
            if invite.access != access:
                invite.access = access
                invite.save()

        return ResponseOk()

    @action(methods=['put'], detail=False, url_path='(?P<note_id>[^/.]+)/update_security', )
    def update_security(self, request, note_id, *args, **kwargs):
        user = self.request.user
        note = Note.objects.filter(pk=note_id, user=user).first()
        if not note:
            raise PermissionDenied(detail='You dont have permission to this note!')
        setting = note.get_settings()
        serializer = NoteSecurityConfigSerializer(setting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['put'], detail=False, url_path='update_other_note/(?P<pk>[^/.]+)', )
    def update_other_note(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    @action(methods=['get'], detail=False, )
    def trash(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(methods=['get'], detail=False, serializer_class=NoteLinkSerializer)
    def accessible_notes(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(methods=['put'], detail=False, url_path='update_access/(?P<access_id>[^/.]+)', )
    def update_access(self, request, access_id, *args, **kwargs):
        user = self.request.user
        note_access = NoteAccess.objects.filter(pk=access_id, note__user=user).first()
        if not note_access:
            raise PermissionDenied(detail='You dont have permission to this note!')
        new_access = request.data.get('access')
        if new_access not in [1, 2, 3, -1]:
            raise BadRequest(detail='Invalid access type')
        if new_access == -1:
            note_access.delete()
        else:
            note_access.access = new_access
            note_access.save()
        return ResponseOk()

    @action(methods=['post'], detail=False, url_path='request_access/(?P<link>[^/.]+)')
    def request_access(self, request, link, *args, **kwargs):
        user = self.request.user

        config: NoteSecurityConfig = NoteSecurityConfig.objects.prefetch_related('note').filter(link=link).first()
        if not config:
            raise NotFound

        if NoteRequestAccess.objects.filter(note_id=config.note_id, user=user,
                                            status=RequestAccessStatuses.pending).exists():
            raise BadRequest(detail="You have a pending request")

        if NoteAccess.objects.filter(note_id=config.note_id, user=user).exists():
            raise BadRequest(detail="You have access already")

        NoteRequestAccess(
            note=config.note,
            user=user,
            type=RequestType.request,
            member_message=request.data.get('member_message')
        ).save()

        return ResponseOk()

    @action(methods=['post'], detail=False, url_path='duplicate/(?P<note_id>[^/.]+)')
    def duplicate(self, request, note_id, *args, **kwargs):
        user = self.request.user
        note: Note = Note.objects.filter(id=note_id, user=user, ).first()
        if not note:
            raise NotFound
        new_note = Note(
            user=user,
            title=note.title + ' (1)',
            editor_data=note.editor_data,
            editor_version=note.editor_version,
            editor_time=note.editor_time,
        )
        new_note.save()
        return Response(NoteSerializer(new_note).data)

    @action(methods=['post'], detail=False, url_path='answer_request_access/(?P<request_id>[^/.]+)')
    def answer_request_access(self, request, request_id, *args, **kwargs):
        user = self.request.user
        access_request = get_object_or_404(
            NoteRequestAccess,
            id=request_id,
            note__user=user,
            type=RequestType.request,
            status=RequestAccessStatuses.pending
        )
        answer = request.data.get('answer')
        if answer == 'accept':
            access_request.accepted()
        elif answer == 'reject':
            access_request.rejected()
        else:
            raise BadRequest(detail="Invalid answer")
        return ResponseOk()


class NoteTemplateViewSet(CustomModelViewSet):
    model = NoteTemplate
    queryset = NoteTemplate.objects.all()
    serializer_class = NoteTemplateSerializer

    def filter_queryset(self, qs):
        if not self.request.user.is_superuser:
            return NoteTemplateFilter(self.request.query_params).qs.filter(user=self.request.user)
        return super().filter_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteAttachmentViewSet(CustomModelViewSet):
    model = NoteAttachment
    queryset = NoteAttachment.objects.all()
    serializer_class = NoteAttachmentSerializer
    disable_views = ['update']

    def filter_queryset(self, qs):
        if not self.request.user.is_superuser:
            return NoteAttachmentFilter(self.request.query_params).qs.filter(note__user=self.request.user)
        return super().filter_queryset(qs)
