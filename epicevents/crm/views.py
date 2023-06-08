from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .permissions import IsAuthenticated, IsClientContact, IsEventSupport
from .models import Client, Contrat, Event, User
from .serializer import ClientSerializer, ClientPutSerializer, \
    ContratSerializer, \
    EventSerializer, EventDetailSerializer


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    put_serializer_class = ClientPutSerializer
    http_method_names = ['get', 'put']
    permission_classes = [IsClientContact]

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return self.put_serializer_class
        return super().get_serializer_class()


class ContratViewset(ModelViewSet):

    serializer_class = ContratSerializer
    http_method_names = ['get', 'put']
    permission_classes = [IsClientContact]

    def get_queryset(self):
        return Contrat.objects.all()


class EventViewset(ModelViewSet):

    serializer_class = EventSerializer
    http_method_names = ['get', 'put']
    permission_classes = [IsClientContact | IsEventSupport]

    def get_queryset(self):
        return Event.objects.all()

