from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client, Contrat, Event, User


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['event_name', 'attendees', 'event_date', 'contrat']


class EventDetailSerializer(EventSerializer):

    class Meta:
        model = Event
        fields = ['event_name', 'attendees', 'event_date', 'contrat', 'notes',
                  'support_contact', 'event_status']


class EventPutSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['event_name', 'attendees', 'event_date', 'notes', 'event_status']

    def validate_event_name(self, value):
        qr = Event.objects.filter(event_name=value)
        if qr.exists():
            raise serializers.ValidationError("Ce nom d'evenement existe déja")
        return value


class ContratSerializer(ModelSerializer):

    event = EventSerializer(many=True)

    class Meta:
        model = Contrat
        fields = ['internal_contrat_number', 'amount', 'client', 'event']


class ContratDetailSerializer(ModelSerializer):

    event = EventSerializer(many=True)

    class Meta:
        model = Contrat
        fields = ['internal_contrat_number', 'status', 'amount', 'payment_due', 'client',
                  'date_created', 'date_updated', 'event']


class ContratPutSerializer(ModelSerializer):

    class Meta:
        model = Contrat
        fields = ['internal_contrat_number', 'amount', 'payment_due', 'status']

    def validate_internal_contrat_number(self, value):
        if Contrat.objects.filter(internal_contrat_number=value).exists():
            raise serializers.ValidationError('Contrat number already exist')
        return value


class ClientSerializer(ModelSerializer):

    contrat = ContratSerializer(many=True)

    class Meta:
        model = Client
        fields = ['company_name', 'email', 'sales_contact', 'client_status', 'contrat']


class ClientDetailSerializer(ModelSerializer):

    contrat = ContratSerializer(many=True)

    class Meta:
        model = Client
        fields = ['company_name', 'first_name', 'last_name', 'email', 'phone',
                  'date_created', 'date_updated',
                  'sales_contact', 'client_status', 'contrat']


class ClientPutSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['company_name', 'first_name', 'last_name', 'email', 'phone', 'client_status']

    def validate_company_name(self, value):
        if Client.objects.filter(company_name=value).exists():
            raise serializers.ValidationError('Company name name already exist')
        return value
