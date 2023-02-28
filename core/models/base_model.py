from django.db import models
from simple_history.models import HistoricalRecords


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    objects = models.Manager()
    active_objects = ActiveManager()

    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def force_delete(self):
        super().delete()

    class Meta:
        abstract = True


class HistoricalBaseModel(BaseModel):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
