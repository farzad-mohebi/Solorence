from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from django.dispatch import receiver

from workspace.history_structure import History
from workspace.models import Note, NoteSecurityConfig


@receiver(post_save, sender=Note)
def note_save(sender, instance: Note, created, **kwargs):
    if not instance.get_settings():
        NoteSecurityConfig(
            note=instance,
            link=NoteSecurityConfig.generate_unique_link()
        ).save()


@receiver(pre_save, sender=Note)
def note_pre_save(sender, instance: Note, **kwargs):
    if not instance.history or type(instance.history) != list:
        instance.history = []

    if len(instance.history) > 0:
        last_history: History = History.create_from_dict(instance.history[0])
        if not last_history.is_read_only and last_history.is_recently():
            instance.history[0] = History(title=instance.title, blocks=instance.editor_data).get_dict()
        else:
            instance.history.insert(0, History(title=instance.title, blocks=instance.editor_data).get_dict())
    else:
        instance.history.insert(0, History(title=instance.title, blocks=instance.editor_data).get_dict())
