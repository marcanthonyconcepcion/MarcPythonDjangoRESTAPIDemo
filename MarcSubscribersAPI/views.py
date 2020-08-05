from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SubscriberSerializer
from .models import Subscriber


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('email_address')
    serializer_class = SubscriberSerializer
