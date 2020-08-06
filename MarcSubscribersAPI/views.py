from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from .serializers import SubscriberProfileSerializer
from .serializers import SubscriberUnauthenticatedProfileSerializer
from .serializers import SubscriberFullCredentialsSerializer
from django.core.mail import send_mail
from django.conf import settings
#from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .models import Subscriber
from .models import Token
import shlex, subprocess, json


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('email_address')
    serializer_class = SubscriberProfileSerializer
    #permission_classes = [permissions.AllowAny, TokenHasReadWriteScope]

    # GET to list all subscribers.
    def list(self, request):
        output_message = self.generate_initial_output_message()
        if 'token' in request.data:
            token_entry = request.data.get('token')
            if Token.objects.filter(token=token_entry).exists():
                serializer = SubscriberProfileSerializer(Subscriber.objects.all(), many=True)
                output_message["user"] = serializer.data
                return Response(output_message, status=status.HTTP_200_OK)
        serializer = SubscriberUnauthenticatedProfileSerializer(Subscriber.objects.all(), many=True)
        output_message["user"] = serializer.data
        return Response(output_message, status=status.HTTP_200_OK)

    # POST to register new subscriber.
    def create(self, request):
        output_message = self.generate_initial_output_message()
        email = request.data.get('email_address')
        if Subscriber.objects.filter(email_address=email).exists():
            output_message["errors"].append({
                    "email_address": ["User e-mail already exists."]
                })
            return Response(output_message, status=status.HTTP_409_CONFLICT)
        serializer = SubscriberFullCredentialsSerializer(data=request.data)
        if not serializer.is_valid():
            output_message["errors"].append(serializer.errors)
            return Response(output_message, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        self.send_token(email)
        output_message["user"] = serializer.data
        return Response(output_message, status=status.HTTP_201_CREATED)

    # GET with index to for user activation.
    def retrieve(self, request, pk=None):
        output_message = self.generate_initial_output_message()
        if 'token' not in request.data:
            output_message["errors"].append({"system": ["Subscriber is not activated. Token required."]})
            return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
        entry = Subscriber.objects.get(pk=pk)
        token_value = request.data.get('token')
        if not Token.objects.filter(token=token_value).exists():
            output_message["errors"].append({"system": ["Subscriber is not activated. Invalid token."]})
            return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
        entry.activation = True
        entry.save()
        serializer = SubscriberProfileSerializer(entry)
        output_message["user"] = serializer.data
        return Response(output_message, status=status.HTTP_200_OK)

    # PUT should not be used.
    def update(self, request, pk=None):
        output_message = self.generate_initial_output_message()
        output_message["errors"].append({"system": ["Illegal Operation."]})
        return Response(output_message, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # PATCH to change password
    def partial_update(self, request, pk=None):
        output_message = self.generate_initial_output_message()
        if 'password' not in request.data:
            output_message["errors"].append({"password": ["Field required."]})
        if 'new_password' not in request.data:
            output_message["errors"].append({"new_password": ["Field required."]})
        if 'token' not in request.data:
            output_message["errors"].append({"token": ["Field required."]})
        if len(output_message["errors"]) > 0:
            return Response(output_message, status=status.HTTP_400_BAD_REQUEST)
        token_value = request.data.get('token')
        if not Token.objects.filter(token=token_value).exists():
            output_message["errors"].append({"token": ["Unauthorized operation. Invalid token."]})
            return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
        entry = Subscriber.objects.get(pk=pk)
        password = request.data.get('password')
        if entry.password != password:
            output_message["errors"].append({"password": ["Invalid user password."]})
            return Response(output_message, status=status.HTTP_400_BAD_REQUEST)
        new_password = request.data.get('new_password')
        entry.password = new_password
        entry.save()
        serializer = SubscriberFullCredentialsSerializer(entry)
        output_message["user"] = serializer.data
        return Response(output_message, status=status.HTTP_200_OK)

    # DELETE should not be used.
    def destroy(self, request, pk=None):
        output_message = self.generate_initial_output_message()
        output_message["errors"].append({"system": ["Illegal Operation."]})
        return Response(output_message, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def generate_initial_output_message(self):
        return {"user": "null", "errors": []}

    def send_email(self, email, token):
        subject = 'send_email'
        message = 'Here is your token authentication to validate your subscriber account.\n{token}.'.format(
            token=token)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)

    def send_token(self, email_address):
        super_username = "concepcion"
        super_password = "marcpassword"
        oauth2_token_url = "http://localhost:8000/o/token/"
        client_id = "lLemOHWG0aXYTa9fRyTYBujLgIAO0qgxxBxFW6JI"
        client_secret = "b2af93KvLTgH3oD4eNBAZbMnpnHOJxmyWpS7mrSXO3xm3lBzyeGIy9t3ose2onNPXYiWGunt99VYu10DqzuzHgtqj6nm5ejtvsCNOhK3d3UuZnA7Z2zPNZIHCwOBsA5E"
        curl_command = "curl -X POST -d 'grant_type=password&username={username}&password={password}' -u{client_id}:{client_secret} {oauth2_token_url}" \
            .format(username=super_username, password=super_password, client_id=client_id, client_secret=client_secret,
                    oauth2_token_url=oauth2_token_url)
        args = shlex.split(curl_command)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        token_value = json.loads(stdout)["access_token"]
        tokens = Token(token=token_value)
        tokens.save()
        #self.send_email(email_address, token)
