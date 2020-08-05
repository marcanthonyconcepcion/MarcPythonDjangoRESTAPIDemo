from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SubscriberSerializer
from .models import Subscriber


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('email_address')
    serializer_class = SubscriberSerializer

    def list(self, request):
        serializer = SubscriberSerializer(Subscriber.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        email = request.data.get('email_address')
        if Subscriber.objects.filter(email_address=email).exists():
            return Response("Subscriber with e-mail {email} already exists.".format(email=email), status=status.HTTP_409_CONFLICT)
        serializer = SubscriberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        entry = Subscriber.objects.get(pk=pk)
        serializer = SubscriberSerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        return Response("Illegal Operation. Totally replacing an existing subscriber is not allowed.", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        if not request.data:
            return Response("Illegal Operation.", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if 'password' not in request.data:
            return Response("Illegal Operation. No new password to change.", status=status.HTTP_400_BAD_REQUEST)
        entry = Subscriber.objects.get(pk=pk)
        password = request.data.get('password')
        entry.password = password
        entry.save()
        serializer = SubscriberSerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        return Response("Illegal Operation. Deleting a subscriber is not allowed.", status=status.HTTP_405_METHOD_NOT_ALLOWED)
