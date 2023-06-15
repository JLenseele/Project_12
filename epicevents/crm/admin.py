from django.contrib import admin
from .models import User, Client, Contrat, Event
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin


class UserAdminConfig(UserAdmin):
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'first_name', 'groups',
                    'is_active', 'is_staff')
    list_filter = ('groups', 'is_active')
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
    radio_fields = {'groups': admin.VERTICAL}

    def save_model(self, request, obj, form, change):
        """
            Check if each competition are already passed or no
            & add keyword 'valid' set on True or False

            :param: competitions: list of competitions
            :return: list of competitions
        """
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
    radio_fields = {'client_status': admin.VERTICAL}

    @admin.action(description="client status = Existant")
    def client_status_ex(self, request, query):
        query.update(client_status="EX")

    @admin.action(description="client status = Potentiel")
    def client_status_po(self, request, query):
        query.update(client_status="PO")

    actions = [client_status_ex, client_status_po]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sales_contact':
            kwargs['queryset'] = User.objects.filter(groups__name__contains='sales')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EventAdminConfig(ModelAdmin):
    ordering = ('-date_created',)
    list_display = ('event_name', 'attendees', 'event_date', 'support_contact', 'contrat', 'event_status')
    list_display_links = ('event_name', 'support_contact', 'contrat')
    list_filter = ('event_date', 'support_contact', 'event_status')
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
    radio_fields = {'event_status': admin.VERTICAL}

    @admin.action(description="event status = Organisation")
    def event_status_or(self, request, query):
        query.update(event_status="OR")

    @admin.action(description="event status = Prêt")
    def event_status_pr(self, request, query):
        query.update(event_status="PR")

    @admin.action(description="event status = Terminé")
    def event_status_te(self, request, query):
        query.update(event_status="TE")

    actions = [event_status_te, event_status_or, event_status_pr]

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
