import uuid

from django.db import models


# Create your models here.


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    cell_id = models.IntegerField()
    reminded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def start_datetime(self):
        new_start_timestamp = self.start_timestamp
        return new_start_timestamp.strftime('%d.%m.%y %H:%M')

    def end_datetime(self):
        new_end_timestamp = self.end_timestamp
        return new_end_timestamp.strftime('%d.%m.%y %H:%M')
