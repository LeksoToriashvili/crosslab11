from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Answer


@receiver(pre_save, sender=Answer)
def ensure_single_accepted_answer(sender, instance, **kwargs):
    if instance.is_accepted:
        # Deselect other answers for the same question
        sender.objects.filter(question=instance.question).update(is_accepted=False)
