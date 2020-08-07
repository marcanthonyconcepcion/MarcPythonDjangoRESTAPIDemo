from django.db import models


class Subscriber(models.Model):
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    activation = models.BooleanField(default=False)

    def __str__(self):
        return self.email_address


class Token(models.Model):
    token = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.token
