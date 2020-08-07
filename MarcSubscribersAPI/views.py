from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from .serializers import SubscriberProfileSerializer
from .serializers import SubscriberUnauthenticatedProfileSerializer
from .serializers import SubscriberFullCredentialsSerializer
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscriber
from .models import Token
import shlex, subprocess, json
from smtplib import SMTPAuthenticationError


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('email_address')
    serializer_class = SubscriberProfileSerializer

    # GET to list all subscribers.
    def list(self, request):
        output_message = self.generate_initial_output_message()
        if 'token' in request.data:
            token_entry = request.data.get('token')
            if Token.objects.filter(token=token_entry).exists():
                serializer = SubscriberProfileSerializer(Subscriber.objects.all(), many=True)
                output_message["user"] = serializer.data
                return Response(output_message, status=status.HTTP_200_OK)
            else:
                output_message["errors"].append({"token": ["Invalid token."]})
                return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
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
        token_value = self.generate_token()
        try:
            self.send_email(email, token_value)
        except SMTPAuthenticationError:
            output_message["errors"].append({"token": ["Server error. Fail to e-mail token. Subscriber not created."]})
            return Response(output_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.save()
        output_message["user"] = serializer.data
        return Response(output_message, status=status.HTTP_201_CREATED)

    # PUT with index to for user activation.
    def update(self, request, pk=None):
        output_message = self.generate_initial_output_message()
        if not Subscriber.objects.filter(pk=pk).exists():
            output_message["errors"].append({"email_address": ["Subscriber does not exist."]})
            return Response(output_message, status=status.HTTP_404_NOT_FOUND)
        if 'token' not in request.data:
            output_message["errors"].append({"token": ["Subscriber is not activated. Token required."]})
            return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
        entry = Subscriber.objects.get(pk=pk)
        token_value = request.data.get('token')
        if not Token.objects.filter(token=token_value).exists():
            output_message["errors"].append({"token": ["Subscriber is not activated. Invalid token."]})
            return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
        if entry.activation:
            output_message["errors"].append({"activation": ["Subscriber has already been activated before."]})
            return Response(output_message, status=status.HTTP_400_BAD_REQUEST)
        entry.activation = True
        entry.save()
        serializer = SubscriberProfileSerializer(entry)
        output_message["user"] = serializer.data
        return Response(output_message, status=status.HTTP_200_OK)

    # GET with index for user login.
    def retrieve(self, request, pk=None):
        output_message = self.generate_initial_output_message()
        if not Subscriber.objects.filter(pk=pk).exists():
            output_message["errors"].append({"email_address": ["Subscriber does not exist."]})
            return Response(output_message, status=status.HTTP_404_NOT_FOUND)
        if 'email_address' not in request.data:
            output_message["errors"].append({"email_address": ["Field required."]})
        if 'password' not in request.data:
            output_message["errors"].append({"password": ["Field required."]})
        if len(output_message["errors"]) > 0:
            return Response(output_message, status=status.HTTP_400_BAD_REQUEST)
        entry = Subscriber.objects.get(pk=pk)
        email = request.data.get('email_address')
        password = request.data.get('password')
        if entry.email_address != email:
            output_message["errors"].append({"email_address": ["E-mail does not match the user's."]})
            return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
        if entry.password != password:
            output_message["errors"].append({"password": ["Password does not match the user's."]})
            return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
        if not entry.activation:
            output_message["errors"].append({"email_address": ["User has not been activated yet."]})
            return Response(output_message, status=status.HTTP_401_UNAUTHORIZED)
        token_value = self.generate_token()
        output_message["user"] = dict({"token": token_value})
        return Response(output_message, status=status.HTTP_200_OK)

    # PATCH to change password
    def partial_update(self, request, pk=None):
        output_message = self.generate_initial_output_message()
        if not Subscriber.objects.filter(pk=pk).exists():
            output_message["errors"].append({"email_address": ["Subscriber does not exist."]})
            return Response(output_message, status=status.HTTP_404_NOT_FOUND)
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
        if not Subscriber.objects.filter(pk=pk).exists():
            output_message["errors"].append({"email_address": ["Subscriber does not exist."]})
            return Response(output_message, status=status.HTTP_404_NOT_FOUND)
        output_message["errors"].append({"email_address": ["Deleting your account through this API is not allowed."]})
        return Response(output_message, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def generate_initial_output_message(self):
        return {"user": "null", "errors": []}

    def send_email(self, email, token):
        subject = 'Your token authentication to access your subscriber account.'
        message = 'Here is your token authentication to validate and to access your subscriber account.\n{token}.'.format(token=token)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)

    def generate_token(self):
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
        return token_value
