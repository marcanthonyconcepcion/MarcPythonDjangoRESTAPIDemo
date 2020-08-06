from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from .serializers import SubscriberSerializer
from django.core.mail import send_mail
from django.conf import settings
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .models import Subscriber


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('email_address')
    serializer_class = SubscriberSerializer
#    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    # GET to list all subscribers.
    def list(self, request):
        output_message = self.generate_initial_output_message()
        serializer = SubscriberSerializer(Subscriber.objects.all(), many=True)
        output_message["user"] = serializer.data
        return Response(output_message, status=status.HTTP_200_OK)

    # POST to register new subscriber.
    def create(self, request):
        output_message = self.generate_initial_output_message()
        email = request.data.get('email_address')
        if Subscriber.objects.filter(email_address=email).exists():
            output_message["errors"].append({
                    "email_address": ["E-mail already exists."]
                })
            return Response(output_message, status=status.HTTP_409_CONFLICT)
        serializer = SubscriberSerializer(data=request.data)
        if not serializer.is_valid():
            output_message["errors"].append(serializer.errors)
            return Response(output_message, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        token = "token"
#       self.send_email(email, token)
        output_message["user"] = serializer.data
        return Response(output_message, status=status.HTTP_201_CREATED)

    # GET with index to for user activation.
    def retrieve(self, request, pk=None):
        output_message = self.generate_initial_output_message()
        entry = Subscriber.objects.get(pk=pk)
        serializer = SubscriberSerializer(entry)
        output_message["user"] = serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            return Response(output_message, status=status.HTTP_400_BAD_REQUEST)
        entry = Subscriber.objects.get(pk=pk)
        password = request.data.get('password')
        entry.password = password
        entry.save()
        serializer = SubscriberSerializer(entry)
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
