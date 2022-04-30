from django.urls import path
from . import views


urlpatterns = [
    path('main/', views.dashboard_view, name='dashboard'),
    path('charts/barchart/', views.get_claimtype_chart, name='barchart'),
    path('charts/barbillchart/', views.get_totalbilled_chart, name='barbillchart')
]