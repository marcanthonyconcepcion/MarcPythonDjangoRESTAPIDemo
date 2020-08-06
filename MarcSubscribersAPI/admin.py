from django.contrib import admin
from .models import Subscriber
from .models import Token


admin.site.register(Subscriber)
admin.site.register(Token)
