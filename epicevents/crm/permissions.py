from rest_framework.permissions import BasePermission
from .models import Client, Contrat, Event

EDIT_METHOD = ['DELETE', 'PUT', 'PATCH']
SAFE_METHOD = ['POST', 'GET']


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)


class IsClientContact(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHOD:
            return True
        if type(obj) == Client:
            return bool(request.user == obj.sales_contact)
        elif type(obj) == Contrat:
            client = obj.client
            return bool(request.user == client.sales_contact)
        elif type(obj) == Event:
            contrat = obj.contrat
            client = contrat.client
            return bool(request.user == client.sales_contact)


class IsEventSupport(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHOD:
            return True
        return bool(request.user == obj.support_contact)