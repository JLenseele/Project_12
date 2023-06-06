from django.contrib import admin
from .models import User, Client, Contrat, Event
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):

    ordering = ('-start_date',)
    list_display = ('email', 'username', 'first_name', 'groups',
                    'is_active', 'is_staff')
    list_filter = ('email', 'username', 'groups')
    search_fields = ('email', 'username', 'groups')
    fieldsets = (
        (None,
         {'fields': (
             'email', 'username', 'first_name',)}),
        ('Permissions',
         {'fields': (
             'is_staff', 'is_active', 'groups')}),
    )
    add_fieldsets = (
        ('User Information',
         {'classes': ('wide',),
          'fields': (
              'email', 'username', 'first_name', 'password',), },),
        ('Groups',
         {'fields': (
             'groups', 'is_active', 'is_staff',), },),
    )
    filter_horizontal = ()


admin.site.register(User, UserAdminConfig)
admin.site.register(Client)
admin.site.register(Contrat)
admin.site.register(Event)
