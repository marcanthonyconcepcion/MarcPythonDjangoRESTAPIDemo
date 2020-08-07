from rest_framework import serializers
from .models import Subscriber, Token


class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        fields = ('token',)


class SubscriberProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('email_address', 'first_name', 'last_name')


class SubscriberUnauthenticatedProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('first_name',)


class SubscriberFullCredentialsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('email_address', 'password', 'first_name', 'last_name')
