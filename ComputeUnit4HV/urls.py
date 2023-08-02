from django.urls import path
from . import views
urlpatterns = [
    path('network/switch/private/create/', views.create_private_switch, name='create_private_switch'),
    path('network/switch/internal/create/', views.create_internal_switch, name='create_internal_switch'),
    path('network/switch/external/create/', views.create_external_switch, name='create_external_switch')
]