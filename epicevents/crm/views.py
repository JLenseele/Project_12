from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsClientContact, IsEventSupport
from django.db import transaction
from .models import Client, Contrat, Event
from .serializer import ClientSerializer, ClientPutSerializer, ClientDetailSerializer, \
    ContratSerializer, ContratPutSerializer, ContratDetailSerializer, \
    EventSerializer, EventDetailSerializer, EventPutSerializer


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    detail_serializer_class = ClientDetailSerializer
    put_serializer_class = ClientPutSerializer
    http_method_names = ['get', 'put', 'post']
    permission_classes = [IsClientContact]

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'create']:
            return self.put_serializer_class
        elif self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = ClientPutSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            if user.groups.name == "sales":
                serializer.save(
                    sales_contact=user
                )
            else:
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class ContratViewset(ModelViewSet):

    serializer_class = ContratSerializer
    detail_serializer_class = ContratDetailSerializer
    put_serializer_class = ContratPutSerializer
    http_method_names = ['get', 'put', 'post']
    permission_classes = [IsClientContact]

    def get_queryset(self):
        return Contrat.objects.filter(client=self.kwargs["client_pk"])

    def get_serializer_class(self):
        if self.action in ['update', 'create']:
            return self.put_serializer_class
        elif self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = ContratPutSerializer(data=request.data)
        client = Client.objects.get(id=self.kwargs["client_pk"])
        print(serializer)
        if serializer.is_valid():
            serializer.save(
                client=client
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class EventViewset(ModelViewSet):

    serializer_class = EventSerializer
    detail_serializer_class = EventDetailSerializer
    put_serializer_class = EventPutSerializer
    http_method_names = ['get', 'put', 'post']
    permission_classes = [IsClientContact | IsEventSupport]

    def get_queryset(self):
        contrats = Contrat.objects.filter(client=self.kwargs["client_pk"])
        for contrat in contrats:
            if contrat.id == int(self.kwargs["contrat_pk"]):
                return Event.objects.filter(contrat=self.kwargs["contrat_pk"])
        return

    def get_serializer_class(self):
        if self.action in ['update', 'create']:
            return self.put_serializer_class
        elif self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = EventPutSerializer(data=request.data)
        contrat = Contrat.objects.get(id=self.kwargs["contrat_pk"])
        if serializer.is_valid():
            serializer.save(
                contrat=contrat
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)
