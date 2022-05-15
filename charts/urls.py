from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('charts/barchart/', views.get_claimtype_chart, name='barchart'),
    path('charts/barbillchart/', views.get_totalbilled_chart, name='barbillchart'),
    path('providerdata/<int:providerID>', views.get_provider_data, name='providerpage'),
    path('providerdata/chart/<int:providerID>', views.get_provider_chart, name='providercharts'),
    path('providerdata/barchart/<int:providerID>', views.get_provider_bar, name='providerbarcharts'),
    path('claimvolume/', views.get_claim_volume, name='claimvolume'),
    # path('claimvolume/linechart', views.get_claim_volume_data, name='claimvolumedata')
    path('claimvolume/linechart/<int:year>', views.get_claim_volume_data, name='claimvolumedata')
]