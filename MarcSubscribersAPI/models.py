from django.db import models


class Subscriber(models.Model):
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    def __str__(self):
        return self.email_address
