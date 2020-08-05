from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SubscriberSerializer
from .models import Subscriber


@api_view(['GET', 'POST', 'PATCH', 'DELETE', 'PUT'])
def subscribers(request):
    # GET is RETURN ALL LIST
    if request.method == 'GET':
        if not request.data:
            serializer = SubscriberSerializer(Subscriber.objects.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            email = request.data.get('email_address')
            if not Subscriber.objects.filter(email_address=email).exists():
                return Response("E-mail Address {email} not found.".format(email=email), status=status.HTTP_404_NOT_FOUND)
            entry = Subscriber.objects.get(email_address=email)
            serializer = SubscriberSerializer(entry)
            return Response(serializer.data, status=status.HTTP_200_OK)
    # POST is REGISTRATION
    elif request.method == 'POST':
        email = request.data.get('email_address')
        if Subscriber.objects.filter(email_address=email).exists():
            return Response("Subscriber with e-mail {email} already exists.".format(email=email), status=status.HTTP_409_CONFLICT)
        serializer = SubscriberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # PATCH is Change Password
    elif request.method == 'PATCH':
        if not request.data:
            return Response("Illegal Operation.", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if 'email_address' not in request.data:
            return Response("Illegal Operation. No e-mail address specified.", status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in request.data:
            return Response("Illegal Operation. No new password to change.", status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email_address')
        if not Subscriber.objects.filter(email_address=email).exists():
            return Response("E-mail Address not found.", status=status.HTTP_404_NOT_FOUND)
        entry = Subscriber.objects.get(email_address=email)
        password = request.data.get('password')
        entry.password = password
        entry.save()
        serializer = SubscriberSerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # DELETE is not allowed.
    elif request.method == 'DELETE':
        return Response("Illegal Operation. Deleting a subscriber is not allowed.", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    # PUT is not allowed.
    elif request.method == 'PUT':
        return Response("Illegal Operation. Totally replacing an existing subscriber is not allowed.", status=status.HTTP_405_METHOD_NOT_ALLOWED)
