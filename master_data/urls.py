from django.urls import path
from master_data.views import StatusListView,StatusDetailView,StatusCreateView, CarrierTypeListView,CarrierTypeCreateView,CarrierTypeDetailView

urlpatterns = [
    # Status
    path('status', StatusListView.as_view(), name='status_list_filter'),
    path('status/add', StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>', StatusDetailView.as_view(), name='status_detail'),
    # Carrier Types
    path('carrier-types', CarrierTypeListView.as_view(), name='carrier_types_list_filter'),
    path('carrier-types/add', CarrierTypeCreateView.as_view(), name='carrier_types_create'),
    path('carrier-types/<int:pk>', CarrierTypeDetailView.as_view(), name='carrier_types_detail'),
]