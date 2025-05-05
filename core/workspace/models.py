import uuid
from uuid import uuid4

from django.db import models
from rest_framework.exceptions import ValidationError

from account.models import User
from utils.models import CustomModel


class Note(CustomModel, models.Model):
    class Meta:
        ordering = ['-pk']

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    editor_data = models.JSONField(max_length=99999, blank=True, null=True)
    editor_version = models.CharField(max_length=50)
    editor_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='editor time')
    history = models.JSONField(max_length=99999, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Deleted at')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    @classmethod
    def serializer_fields(cls, excludes=None) -> list:
        return super().serializer_fields(['history'])

    def get_settings(self):
        return getattr(self, 'settings', None)

    def __str__(self):
        return self.title

    def clean(self):
        if type(self.editor_data) is not list:
            raise ValidationError(
                {"editor_data": "must be a list of blocks!"}
            )


class NoteTemplate(CustomModel, models.Model):
    class Meta:
        ordering = ['-pk']

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')
    editor_data = models.JSONField(max_length=99999)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.title

    def clean(self):
        if type(self.editor_data) is not list:
            raise ValidationError(
                {"editor_data": "must be a list of blocks!"}
            )


class SecurityStatus(models.IntegerChoices):
    private = 1, 'private'
    public = 2, 'public'


class AccessTypes(models.IntegerChoices):
    viewer = 1, 'viewer'
    commenter = 2, 'commenter'
    editor = 3, 'editor'


class NoteSecurityConfig(CustomModel, models.Model):
    class Meta:
        ordering = ['-note_id']

    note = models.OneToOneField(Note, related_name='settings', on_delete=models.CASCADE, )
    status = models.IntegerField(choices=SecurityStatus.choices, default=SecurityStatus.private.value)
    public_joiners_access = models.IntegerField(choices=AccessTypes.choices, default=AccessTypes.viewer.value)
    link = models.CharField(max_length=64, unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')

    def __str__(self):
        return 'Security Settings of ' + str(self.note_id)

    @property
    def is_public(self):
        return self.status == SecurityStatus.public

    @property
    def is_private(self):
        return self.status == SecurityStatus.private

    @staticmethod
    def generate_unique_link():
        link = (str(uuid4()) + '-' + str(uuid4()))[0:64]
        if NoteSecurityConfig.objects.filter(link=link).exists():
            return NoteSecurityConfig.generate_unique_link()
        return link


class RequestAccessStatuses(models.IntegerChoices):
    pending = 0, 'pending'
    accepted = 1, 'accepted'
    rejected = 2, 'rejected'


class NoteAccess(CustomModel, models.Model):
    class Meta:
        ordering = ['-note_id']

    note = models.ForeignKey(Note, related_name='access', on_delete=models.CASCADE, )
    user = models.ForeignKey(User, related_name='access', on_delete=models.CASCADE, )
    access = models.IntegerField(choices=AccessTypes.choices, default=AccessTypes.viewer.value, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.get_access_display() + ' - ' + self.user_id + ' - ' + self.note_id


class RequestType(models.IntegerChoices):
    request = 0, 'request'
    invite = 1, 'invite'


class NoteRequestAccess(CustomModel, models.Model):
    class Meta:
        ordering = ['-note_id']

    note = models.ForeignKey(Note, related_name='requests', on_delete=models.CASCADE, )
    user = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE, )
    access = models.IntegerField(choices=AccessTypes.choices, default=AccessTypes.viewer.value, blank=True)
    owner_message = models.TextField(max_length=300, blank=True)
    member_message = models.TextField(max_length=300, blank=True)  # Request|Reply Msg of the user who isn't Note Owner
    status = models.IntegerField(choices=RequestAccessStatuses.choices, default=RequestAccessStatuses.pending.value)
    type = models.IntegerField(choices=RequestType.choices, default=RequestType.request.value)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.get_access_display() + ' - ' + str(self.user_id) + ' - ' + str(self.note_id)

    def accepted(self):
        NoteAccess.objects.get_or_create(note=self.note, user=self.user, )
        self.status = RequestAccessStatuses.accepted
        self.save()

    def rejected(self):
        self.status = RequestAccessStatuses.rejected
        self.save()


def note_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'note/{0}/{1}'.format(instance.note.id, filename)


class NoteAttachment(models.Model):
    class Meta:
        ordering = ['-note_id']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    note = models.ForeignKey(Note, related_name='attachments', on_delete=models.CASCADE, )
    image = models.FileField(upload_to=note_directory_path)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def delete(self, *args, **kwargs):
        """
        Delete must be overridden because the inherited delete method does not call `self.file.delete()`.
        """
        self.image.delete()
        super(NoteAttachment, self).delete(*args, **kwargs)
