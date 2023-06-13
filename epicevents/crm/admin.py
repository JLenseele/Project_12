from django.contrib import admin
from .models import User, Client, Contrat, Event
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin


class UserAdminConfig(UserAdmin):

    ordering = ('-start_date',)
    list_display = ('email', 'username', 'first_name', 'groups',
                    'is_active', 'is_staff')
    list_filter = ('email', 'username', 'groups')
    search_fields = ('email', 'username', 'groups')
    fieldsets = [
        ('User Information',
         {
             'fields': [('email', 'username'), ('first_name', 'last_name')], }, ),
        ('Permissions',
         {
             'fields': ['is_staff', 'is_active', 'groups'], }, ),
    ]
    add_fieldsets = (
        ('User Information',
         {'classes': ('wide',),
          'fields': (
              'email', 'username', 'first_name', 'password1', 'password2'), },),
        ('Groups',
         {'fields': (
             'groups', 'is_active', 'is_staff',), },),
    )
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if change:
            saler = User.objects.filter(email=obj.email)
            old_team = saler[0].groups
            if old_team != obj.groups:
                clients = Client.objects.filter(sales_contact__in=saler)
                for client in clients:
                    client.sales_contact = None
                    client.save()
        super().save_model(request, obj, form, change)


class ClientAdminConfig(ModelAdmin):
    ordering = ('-date_created',)
    list_display = ('company_name', 'email', 'sales_contact', 'client_status', 'date_created', 'date_updated')
    list_filter = ('sales_contact', 'client_status')
    search_fields = ('company_name', 'email', 'sales_contact')

    fieldsets = [
        ('Client Information',
         {
             'fields': ['company_name', ('first_name', 'last_name')], },),
        ('Contact',
         {
             'fields': ['email', 'phone', 'sales_contact', 'client_status'], },),
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sales_contact':
            kwargs['queryset'] = User.objects.filter(groups__name__contains='sales')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EventAdminConfig(ModelAdmin):
    ordering = ('-date_created',)
    list_display = ('event_name', 'attendees', 'event_date', 'support_contact', 'contrat')
    list_filter = ('event_date', 'support_contact')
    search_fields = ('event_name',)

    fieldsets = [
        ('Event Information',
         {
             'fields': ['event_name', 'attendees', 'event_date'], },),
        ('Links',
         {
             'fields': ['contrat', 'support_contact'], },),
        ('More',
         {
             'fields': ['event_status', 'notes'], },),
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'support_contact':
            kwargs['queryset'] = User.objects.filter(groups__name__contains='support')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ContratAdminConfig(ModelAdmin):
    ordering = ('-date_created',)
    list_display = ('internal_contrat_number', 'client', 'amount', 'payment_due', 'status')
    list_filter = ('client', 'status')
    search_fields = ('client',)

    fieldsets = [
        ('Contrat Information',
         {
             'fields': ['internal_contrat_number', 'amount', 'payment_due', 'status'], },),
        ('Links',
         {
             'fields': ['client'], },),
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':
            kwargs['queryset'] = Client.objects.filter(client_status='EX')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(User, UserAdminConfig)
admin.site.register(Client, ClientAdminConfig)
admin.site.register(Contrat, ContratAdminConfig)
admin.site.register(Event, EventAdminConfig)
