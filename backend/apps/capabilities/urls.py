from django.urls import path

from apps.capabilities.views import CapabilitiesView, CapabilitiesValidateView

app_name = 'capabilities'

urlpatterns = [
    path('', CapabilitiesView.as_view(), name='capabilities'),
    path('validate', CapabilitiesValidateView.as_view(), name='capabilities-validate'),
]

