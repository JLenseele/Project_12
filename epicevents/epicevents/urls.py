"""
URL configuration for epicevents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from crm.views import ClientViewset, ContratViewset, EventViewset

router = routers.SimpleRouter()
router.register(r'client', ClientViewset, basename='client')

client_router = routers.NestedSimpleRouter(router, r'client', lookup='client')
client_router.register(r'contrat', ContratViewset, basename='contrat')

contrat_router = routers.NestedSimpleRouter(client_router, r'contrat', lookup='contrat')
contrat_router.register(r'event', EventViewset, basename='event')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/', include(client_router.urls)),
    path('api/', include(contrat_router.urls)),
]
