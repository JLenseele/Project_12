from django.db import migrations


def create_groups(apps, shema_migration):
    User = apps.get_model('crm', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    add_client = Permission.objects.get(codename='add_client')
    change_client = Permission.objects.get(codename='change_client')
    delete_client = Permission.objects.get(codename='delete_client')
    view_client = Permission.objects.get(codename='view_client')

    add_contrat = Permission.objects.get(codename='add_contrat')
    change_contrat = Permission.objects.get(codename='change_contrat')
    delete_contrat = Permission.objects.get(codename='delete_contrat')
    view_contrat = Permission.objects.get(codename='view_contrat')

    add_event = Permission.objects.get(codename='add_event')
    change_event = Permission.objects.get(codename='change_event')
    delete_event = Permission.objects.get(codename='delete_event')
    view_event = Permission.objects.get(codename='view_event')

    add_user = Permission.objects.get(codename='add_user')
    change_user = Permission.objects.get(codename='change_user')
    delete_user = Permission.objects.get(codename='delete_user')
    view_user = Permission.objects.get(codename='view_user')

    management_permissions = [
        add_client,
        change_client,
        delete_client,
        view_client,
        add_user,
        change_user,
        delete_user,
        view_user
    ]
    sales_permissions = [
        add_contrat,
        change_contrat,
        delete_contrat,
        view_contrat
    ]
    support_permissions = [
        add_event,
        change_event,
        delete_event,
        view_event
    ]

    management = Group(name='management')
    management.save()

    sales = Group(name='sales')
    sales.save()

    support = Group(name='support')
    support.save()

    management.permissions.set(management_permissions)
    sales.permissions.set(sales_permissions)
    support.permissions.set(support_permissions)

    for user in User.objects.all():
        if user.groups == 'MANAGEMENT':
            management.user_set.add(user)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
