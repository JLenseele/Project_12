from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client, Contrat, Event, User


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['event_name', 'attendees', 'event_date', 'contrat']


class EventDetailSerializer(EventSerializer):

    def validate_event_name(self, value):
        if Event.objects.filter(event_name=value).exists():
            raise serializers.ValidationError('Event name already exist')


class ContratSerializer(ModelSerializer):

    event = EventSerializer(many=True)

    class Meta:
        model = Contrat
        fields = ['internal_contrat_number', 'amount', 'client', 'event']


class ClientSerializer(ModelSerializer):

    contrat = ContratSerializer(many=True)

    class Meta:
        model = Client
        fields = ['company_name', 'email', 'sales_contact', 'client_status', 'contrat']


class ClientPutSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['company_name', 'first_name', 'last_name', 'email', 'phone', 'client_status']
