from rest_framework.permissions import BasePermission
from .models import Client, Contrat, Event

EDIT_METHOD = ['DELETE', 'PUT', 'PATCH', 'POST']
SAFE_METHOD = ['GET']


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)


class IsClientContact(IsAuthenticated):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            print(user.groups)
            if user.groups.name == 'sales':
                return True

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

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == 'POST':
                return False
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHOD:
            return True
        return bool(request.user == obj.support_contact)
