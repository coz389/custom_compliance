from django.urls import path
from master_data.views import (
    StatusListView,StatusDetailView,StatusCreateView, CarrierTypeListView,CarrierTypeCreateView,CarrierTypeDetailView,
    CountryDropdownView, StateDropdownView,CityCreateView, CityDetailView, CityListView,
    ContainerCreateView, ContainerDetailView, ContainerListView,
    EquipmentCreateView, EquipmentDetailView, EquipmentListView,
    SeaportCreateView, SeaportDetailView, SeaportListView
)

urlpatterns = [
    # Country City States
    path('country/list', CountryDropdownView.as_view(), name='country-list'),
    path('states/<int:country_id>', StateDropdownView.as_view(), name='state-list'),
    path('cities/list', CityListView.as_view(), name='city-list'),
    path('cities/add', CityCreateView.as_view(), name='city-create'),
    path('cities/<int:pk>', CityDetailView.as_view(), name='city-detail'),
    # Containers
    path('containers/list', ContainerListView.as_view(), name='container-list'),
    path('containers/add', ContainerCreateView.as_view(), name='container-create'),
    path('containers/<int:pk>', ContainerDetailView.as_view(), name='container-detail'),
    # Equipment
    path('equipment/list', EquipmentListView.as_view(), name='equipment-list'),
    path('equipment/add', EquipmentCreateView.as_view(), name='equipment-create'),
    path('equipment/<int:pk>', EquipmentDetailView.as_view(), name='equipment-detail'),
    # Seaports
    path('seaports/list', SeaportListView.as_view(), name='seaport-list'),
    path('seaports/add', SeaportCreateView.as_view(), name='seaport-create'),
    path('seaports/<int:pk>', SeaportDetailView.as_view(), name='seaport-detail'),
    # Status
    path('status', StatusListView.as_view(), name='status_list_filter'),
    path('status/add', StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>', StatusDetailView.as_view(), name='status_detail'),
    # Carrier Types
    path('carrier-types', CarrierTypeListView.as_view(), name='carrier_types_list_filter'),
    path('carrier-types/add', CarrierTypeCreateView.as_view(), name='carrier_types_create'),
    path('carrier-types/<int:pk>', CarrierTypeDetailView.as_view(), name='carrier_types_detail'),
]

